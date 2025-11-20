'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { authAPI } from '@/lib/api';
import { LogOut, User } from 'lucide-react';

export function Navbar() {
  const router = useRouter();

  const handleLogout = async () => {
    try {
      await authAPI.logout();
      localStorage.removeItem('session_id');
      router.push('/login');
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <nav className="border-b bg-background">
      <div className="container mx-auto px-4">
        <div className="flex h-16 items-center justify-between">
          <div className="flex items-center space-x-8">
            <Link href="/dashboard" className="text-xl font-bold">
              Newton Autopilot
            </Link>
            <div className="hidden md:flex space-x-4">
              <Link href="/dashboard">
                <Button variant="ghost">Dashboard</Button>
              </Link>
              <Link href="/assignments">
                <Button variant="ghost">Assignments</Button>
              </Link>
              <Link href="/schedule">
                <Button variant="ghost">Schedule</Button>
              </Link>
              <Link href="/performance">
                <Button variant="ghost">Performance</Button>
              </Link>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            <Button variant="ghost" size="icon">
              <User className="h-5 w-5" />
            </Button>
            <Button variant="ghost" size="icon" onClick={handleLogout}>
              <LogOut className="h-5 w-5" />
            </Button>
          </div>
        </div>
      </div>
    </nav>
  );
}
