'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { assignmentsAPI } from '@/lib/api';
import useSWR from 'swr';
import { Clock, AlertCircle } from 'lucide-react';
import { formatDateTime } from '@/lib/utils';
import Link from 'next/link';

export function DeadlineWidget() {
  const { data, isLoading } = useSWR('/assignments?status=pending&limit=10', () =>
    assignmentsAPI.list({ status: 'pending', limit: 10 }).then((res) => res.data)
  );

  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Upcoming Deadlines</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-muted-foreground">Loading...</div>
        </CardContent>
      </Card>
    );
  }

  const assignments = (data || [])
    .filter((a: any) => a.due_date)
    .sort((a: any, b: any) =>
      new Date(a.due_date).getTime() - new Date(b.due_date).getTime()
    )
    .slice(0, 5);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Upcoming Deadlines</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {assignments.length === 0 ? (
            <div className="text-center text-muted-foreground py-8">
              No pending assignments
            </div>
          ) : (
            assignments.map((assignment: any) => {
              const dueDate = new Date(assignment.due_date);
              const hoursUntilDue = (dueDate.getTime() - Date.now()) / (1000 * 60 * 60);
              const isUrgent = hoursUntilDue < 24;

              return (
                <div
                  key={assignment.hash}
                  className="flex items-start justify-between p-3 rounded-lg border"
                >
                  <div className="flex-1">
                    <div className="font-medium">{assignment.title}</div>
                    <div className="flex items-center gap-2 mt-1 text-sm text-muted-foreground">
                      {isUrgent && <AlertCircle className="h-4 w-4 text-red-500" />}
                      <Clock className="h-4 w-4" />
                      {formatDateTime(assignment.due_date)}
                    </div>
                    <div className="flex items-center gap-2 mt-1 text-xs">
                      <span className="text-muted-foreground">
                        {assignment.questions_solved}/{assignment.questions_total} completed
                      </span>
                      <span className="text-muted-foreground">•</span>
                      <span className="text-yellow-600">{assignment.xp} XP</span>
                    </div>
                  </div>
                  <Link href={`/assignments/${assignment.hash}?course=${assignment.course_hash}`}>
                    <Button size="sm" variant="outline">
                      Solve
                    </Button>
                  </Link>
                </div>
              );
            })
          )}
        </div>
      </CardContent>
    </Card>
  );
}
