'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { BookOpen, Calendar, Zap, BarChart } from 'lucide-react';
import Link from 'next/link';

export function QuickActions() {
  const actions = [
    {
      label: 'Solve Assignments',
      href: '/assignments',
      icon: BookOpen,
      color: 'bg-blue-500',
    },
    {
      label: 'View Schedule',
      href: '/schedule',
      icon: Calendar,
      color: 'bg-green-500',
    },
    {
      label: 'AI Solver',
      href: '/solver',
      icon: Zap,
      color: 'bg-purple-500',
    },
    {
      label: 'Performance',
      href: '/performance',
      icon: BarChart,
      color: 'bg-orange-500',
    },
  ];

  return (
    <Card>
      <CardHeader>
        <CardTitle>Quick Actions</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 gap-3">
          {actions.map((action) => {
            const Icon = action.icon;
            return (
              <Link key={action.label} href={action.href}>
                <Button
                  variant="outline"
                  className="w-full h-auto flex-col gap-2 p-4"
                >
                  <div className={`${action.color} text-white p-3 rounded-lg`}>
                    <Icon className="h-6 w-6" />
                  </div>
                  <span className="text-sm">{action.label}</span>
                </Button>
              </Link>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}
