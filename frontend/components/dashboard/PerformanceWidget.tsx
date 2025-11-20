'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { performanceAPI } from '@/lib/api';
import useSWR from 'swr';
import { TrendingUp, Award, Calendar, Flame } from 'lucide-react';

export function PerformanceWidget() {
  const { data, isLoading } = useSWR('/performance/overview', () =>
    performanceAPI.overview().then((res) => res.data)
  );

  if (isLoading) {
    return (
      <Card className="col-span-2">
        <CardHeader>
          <CardTitle>Performance Overview</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-muted-foreground">Loading...</div>
        </CardContent>
      </Card>
    );
  }

  const stats = [
    {
      label: 'Attendance',
      value: `${data?.lecture_attendance || 0}%`,
      icon: Calendar,
      color: 'text-blue-500',
    },
    {
      label: 'Assignments',
      value: `${data?.assignments_completed || 0}%`,
      icon: TrendingUp,
      color: 'text-green-500',
    },
    {
      label: 'Total XP',
      value: data?.total_xp || 0,
      icon: Award,
      color: 'text-yellow-500',
    },
    {
      label: 'Streak',
      value: `${data?.streak_days || 0} days`,
      icon: Flame,
      color: 'text-orange-500',
    },
  ];

  return (
    <Card className="col-span-2">
      <CardHeader>
        <CardTitle>Performance Overview</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {stats.map((stat) => {
            const Icon = stat.icon;
            return (
              <div key={stat.label} className="flex flex-col items-center p-4 rounded-lg bg-muted">
                <Icon className={`h-8 w-8 ${stat.color} mb-2`} />
                <div className="text-2xl font-bold">{stat.value}</div>
                <div className="text-sm text-muted-foreground">{stat.label}</div>
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}
