'use client';

import { Layout } from '@/components/layout/Layout';
import { PerformanceWidget } from '@/components/dashboard/PerformanceWidget';
import { ScheduleWidget } from '@/components/dashboard/ScheduleWidget';
import { DeadlineWidget } from '@/components/dashboard/DeadlineWidget';
import { QuickActions } from '@/components/dashboard/QuickActions';

export default function DashboardPage() {
  return (
    <Layout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <p className="text-muted-foreground">
            Welcome to Newton Autopilot - Your AI-powered learning assistant
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <PerformanceWidget />
          <QuickActions />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <ScheduleWidget />
          <DeadlineWidget />
        </div>
      </div>
    </Layout>
  );
}
