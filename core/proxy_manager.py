"""
Proxy Manager for providing proxy configuration.

Note: If using a rotating proxy provider (like Bright Data, Oxylabs, etc.),
the provider handles IP rotation automatically on each request.
"""

import logging
import time
from typing import Optional, Dict
from django.conf import settings

logger = logging.getLogger(__name__)


class ProxyManager:
    """
    Provides proxy configuration for web scraping requests.
    
    This is a simplified version that assumes the proxy provider
    handles rotation automatically. No blacklisting or rotation needed.
    """
    
    def __init__(self):
        self.proxies = self._load_proxies()
        self.proxy_url = self.proxies[0] if self.proxies else None
        self._proxy_index = 0
        self._failed_until = {}
        self._failure_cooldown = float(
            settings.SCRAPER_SETTINGS.get('PROXY_FAILURE_COOLDOWN', 0.5)
        )
        self._fallback_direct = bool(
            settings.SCRAPER_SETTINGS.get('PROXY_FALLBACK_DIRECT', True)
        )
        
    def _load_proxy(self) -> Optional[str]:
        """Load proxy from settings."""
        proxies = self._load_proxies()
        return proxies[0] if proxies else None

    def _load_proxies(self):
        """Load and normalize all configured proxy URLs."""
        proxies = settings.SCRAPER_SETTINGS.get('PROXIES', [])
        if isinstance(proxies, str):
            proxies = [p.strip() for p in proxies.split(',') if p.strip()]
        return list(dict.fromkeys(proxies or []))
    
    def get_proxy(self) -> Optional[Dict[str, str]]:
        """
        Get the configured proxy.
        
        Returns:
            Dictionary with 'http' and 'https' keys, or None if no proxy configured.
        """
        if not self.proxies:
            logger.debug("No proxy configured. Requests will be made directly.")
            return None

        now = time.monotonic()
        for offset in range(len(self.proxies)):
            index = (self._proxy_index + offset) % len(self.proxies)
            proxy = self.proxies[index]
            if now >= self._failed_until.get(proxy, 0):
                self._proxy_index = index
                self.proxy_url = proxy
                logger.debug("Using proxy %s of %s", index + 1, len(self.proxies))
                return {'http': proxy, 'https': proxy}

        if self._fallback_direct:
            logger.warning("All configured proxies are temporarily unavailable; using direct connection")
            return None

        return {'http': self.proxy_url, 'https': self.proxy_url}
    
    def get_random_proxy(self) -> Optional[Dict[str, str]]:
        """Alias for get_proxy() for backward compatibility."""
        return self.get_proxy()
    
    def mark_proxy_failed(self, proxy_url: str):
        """Temporarily bypass a proxy that failed to connect or authenticate."""
        if proxy_url:
            self._failed_until[proxy_url] = time.monotonic() + self._failure_cooldown
            if proxy_url in self.proxies:
                self._proxy_index = (self.proxies.index(proxy_url) + 1) % len(self.proxies)
            logger.warning(
                "Proxy request failed; rotating away for %.0f seconds",
                self._failure_cooldown,
            )
    
    def mark_proxy_success(self, proxy_url: str):
        """No-op: Provider handles rotation."""
        pass
    
    def get_proxy_count(self) -> int:
        """Return 1 if proxy configured, 0 otherwise."""
        return len(self.proxies)
    
    def get_available_proxy_count(self) -> int:
        """Return 1 if proxy configured, 0 otherwise."""
        return 1 if self.get_proxy() else 0


# Singleton instance
proxy_manager = ProxyManager()
