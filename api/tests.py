"""
Tests for the Zillow scraper API.
"""

from unittest.mock import patch, MagicMock
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

from api.serializers import AgentSerializer, PropertySerializer, ReviewSerializer
from core.proxy_manager import ProxyManager
from core.user_agent_manager import UserAgentManager
from scrapers.base import BaseScraper
from curl_cffi.requests.errors import RequestsError


class SerializerTests(TestCase):
    """Tests for API serializers."""
    
    def test_agent_serializer_valid(self):
        """Test AgentSerializer with valid data."""
        data = {
            'name': 'John Doe',
            'url': 'https://www.zillow.com/profile/johndoe',
            'location': 'Los Angeles, CA',
        }
        serializer = AgentSerializer(data=data)
        self.assertTrue(serializer.is_valid())
    
    def test_agent_serializer_invalid(self):
        """Test AgentSerializer with invalid data."""
        data = {'location': 'Los Angeles'}  # Missing required fields
        serializer = AgentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
    
    def test_property_serializer_valid(self):
        """Test PropertySerializer with valid data."""
        data = {
            'zpid': 123456,
            'address': '123 Main St',
            'url': 'https://www.zillow.com/homedetails/123_zpid',
            'price': 500000.0,
            'beds': 3,
            'baths': 2,
            'sqft': 1500,
        }
        serializer = PropertySerializer(data=data)
        self.assertTrue(serializer.is_valid())
    
    def test_review_serializer_valid(self):
        """Test ReviewSerializer with valid data."""
        data = {
            'zuid': 'user123',
            'rating': 5,
            'review': 'Great agent!',
        }
        serializer = ReviewSerializer(data=data)
        self.assertTrue(serializer.is_valid())


class ProxyManagerTests(TestCase):
    """Tests for the proxy manager."""
    
    @patch('core.proxy_manager.settings')
    def test_no_proxies_returns_none(self, mock_settings):
        """Test that get_proxy returns None when no proxies configured."""
        mock_settings.SCRAPER_SETTINGS = {'PROXIES': []}
        manager = ProxyManager()
        self.assertIsNone(manager.get_proxy())
    
    @patch('core.proxy_manager.settings')
    def test_proxy_rotation(self, mock_settings):
        """Test proxy configuration."""
        mock_settings.SCRAPER_SETTINGS = {
            'PROXIES': ['http://proxy1:8080', 'http://proxy2:8080']
        }
        
        manager = ProxyManager()
        proxy = manager.get_proxy()
        
        self.assertIsNotNone(proxy)
        self.assertEqual(proxy['http'], 'http://proxy1:8080')
        self.assertEqual(proxy['https'], 'http://proxy1:8080')

    @patch('core.proxy_manager.settings')
    def test_failed_proxy_is_temporarily_bypassed(self, mock_settings):
        """A failed proxy must not keep all endpoints unavailable."""
        mock_settings.SCRAPER_SETTINGS = {
            'PROXIES': ['http://proxy1:8080'],
            'PROXY_FALLBACK_DIRECT': True,
            'PROXY_FAILURE_COOLDOWN': 60,
        }
        manager = ProxyManager()
        self.assertIsNotNone(manager.get_proxy())
        manager.mark_proxy_failed('http://proxy1:8080')
        self.assertIsNone(manager.get_proxy())


class UserAgentManagerTests(TestCase):
    """Tests for the user-agent manager."""
    
    def test_get_random_user_agent(self):
        """Test that get_random_user_agent returns a string."""
        manager = UserAgentManager()
        ua = manager.get_random_user_agent()
        
        self.assertIsInstance(ua, str)
        self.assertGreater(len(ua), 0)
    
    def test_get_chrome_user_agent(self):
        """Test Chrome user agent contains Chrome."""
        manager = UserAgentManager()
        ua = manager.get_chrome_user_agent()
        
        self.assertIn('Chrome', ua)


class APIEndpointTests(APITestCase):
    """Integration tests for API endpoints."""
    
    @patch('api.views.agent_scraper')
    def test_agent_by_location(self, mock_scraper):
        """Test agentBylocation endpoint."""
        mock_scraper.get_agents_by_location.return_value = {
            'results': [
                {'name': 'Test Agent', 'url': 'http://test.com', 'location': 'LA'}
            ],
            'total_results': 1,
            'current_page': 1
        }
        response = self.client.get('/agentBylocation', {'location': 'los-angeles'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'Test Agent')
    
    @patch('api.views.property_scraper')
    def test_by_location(self, mock_scraper):
        """Test bylocation endpoint."""
        mock_scraper.search_by_location.return_value = {
            'results': [
                {
                    'zpid': 123,
                    'address': '123 Test St',
                    'url': 'http://test.com',
                    'price': 500000,
                    'beds': 3,
                    'baths': 2,
                    'sqft': 1500,
                }
            ],
            'total_results': 1,
            'current_page': 1
        }
        
        response = self.client.get('/bylocation', {'location': 'seattle-wa'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
    
    @patch('api.views.property_scraper')
    def test_autocomplete(self, mock_scraper):
        """Test autocomplete endpoint."""
        mock_scraper.autocomplete.return_value = [
            {'display': 'Los Angeles, CA', 'type': 'city', 'id': '123'}
        ]
        
        response = self.client.get('/autocomplete', {'q': 'los'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_autocomplete_missing_query(self):
        """Test autocomplete endpoint without query."""
        response = self.client.get('/autocomplete')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status_code'], 400)
    
    def test_by_coordinates_missing_params(self):
        """Test bycoordinates endpoint without required params."""
        response = self.client.get('/bycoordinates')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status_code'], 400)
    
    def test_agent_info_missing_params(self):
        """Test agentInfo endpoint without required params."""
        response = self.client.get('/agentInfo')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status_code'], 400)


class ProxyFallbackTests(TestCase):
    """Regression tests for CONNECT tunnel/authentication failures."""

    @patch('scrapers.base.session_pool')
    @patch('scrapers.base.proxy_manager')
    def test_request_retries_without_proxy_after_407(self, mock_proxy_manager, mock_pool):
        proxy = {'http': 'http://proxy:8080', 'https': 'http://proxy:8080'}
        mock_proxy_manager.get_proxy.side_effect = [proxy, None]
        session = MagicMock()
        session.request.side_effect = [
            RequestsError('curl: (56) CONNECT tunnel failed, response 407'),
            MagicMock(status_code=200, content=b'ok', text='ok', raise_for_status=lambda: None),
        ]
        mock_pool.get_session.return_value = session

        response = BaseScraper().get('https://www.zillow.com/homes/123456/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(session.request.call_args_list[0].kwargs['proxies'], proxy)
        self.assertIsNone(session.request.call_args_list[1].kwargs['proxies'])
