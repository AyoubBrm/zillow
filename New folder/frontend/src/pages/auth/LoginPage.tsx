import React from 'react';
import { Lock, Mail } from 'lucide-react';
import Button from '../../components/ui/Button';

const LoginPage = () => {
  return (
    <div className="w-full max-w-md">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-white">Welcome back</h2>
        <p className="text-slate-400 mt-2">Sign in to your LedgerAI account</p>
      </div>

      <form className="space-y-4" onSubmit={(e) => e.preventDefault()}>
        <div>
          <label className="block text-sm font-medium text-slate-300 mb-1">Email</label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Mail className="h-5 w-5 text-slate-500" />
            </div>
            <input
              type="email"
              className="block w-full pl-10 pr-3 py-2 border border-slate-700 rounded-lg leading-5 bg-slate-800/50 text-slate-300 placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-violet-500 focus:border-violet-500 sm:text-sm transition duration-150 ease-in-out"
              placeholder="you@example.com"
              defaultValue="demo@ledgerai.app"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-300 mb-1">Password</label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Lock className="h-5 w-5 text-slate-500" />
            </div>
            <input
              type="password"
              className="block w-full pl-10 pr-3 py-2 border border-slate-700 rounded-lg leading-5 bg-slate-800/50 text-slate-300 placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-violet-500 focus:border-violet-500 sm:text-sm transition duration-150 ease-in-out"
              placeholder="••••••••"
              defaultValue="password123"
            />
          </div>
        </div>

        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <input
              id="remember_me"
              type="checkbox"
              className="h-4 w-4 bg-slate-800 border-slate-700 rounded text-violet-500 focus:ring-violet-500"
            />
            <label htmlFor="remember_me" className="ml-2 block text-sm text-slate-400">
              Remember me
            </label>
          </div>
          <div className="text-sm">
            <a href="#" className="font-medium text-violet-400 hover:text-violet-300">
              Forgot your password?
            </a>
          </div>
        </div>

        <div className="pt-2">
          <Button className="w-full" variant="primary" onClick={() => window.location.href = '/'}>
            Sign in
          </Button>
        </div>
      </form>
    </div>
  );
};

export default LoginPage;
