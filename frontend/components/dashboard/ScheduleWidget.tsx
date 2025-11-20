'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { scheduleAPI } from '@/lib/api';
import useSWR from 'swr';
import { Clock, MapPin, ExternalLink } from 'lucide-react';
import { formatTime, getTimeUntil } from '@/lib/utils';

export function ScheduleWidget() {
  const { data, isLoading } = useSWR('/schedule/today', () =>
    scheduleAPI.today().then((res) => res.data)
  );

  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Today's Schedule</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-muted-foreground">Loading...</div>
        </CardContent>
      </Card>
    );
  }

  const classes = data || [];

  return (
    <Card>
      <CardHeader>
        <CardTitle>Today's Schedule</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {classes.length === 0 ? (
            <div className="text-center text-muted-foreground py-8">
              No classes scheduled for today
            </div>
          ) : (
            classes.slice(0, 5).map((classItem: any) => (
              <div
                key={classItem.hash}
                className="flex items-start justify-between p-3 rounded-lg border"
              >
                <div className="flex-1">
                  <div className="font-medium">{classItem.subject}</div>
                  <div className="flex items-center gap-4 mt-1 text-sm text-muted-foreground">
                    <div className="flex items-center gap-1">
                      <Clock className="h-4 w-4" />
                      {formatTime(classItem.start_timestamp)}
                    </div>
                    {classItem.room && (
                      <div className="flex items-center gap-1">
                        <MapPin className="h-4 w-4" />
                        {classItem.room}
                      </div>
                    )}
                  </div>
                  <div className="text-xs text-muted-foreground mt-1">
                    {getTimeUntil(classItem.start_timestamp)}
                  </div>
                </div>
                {classItem.join_url && (
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => window.open(classItem.join_url, '_blank')}
                  >
                    <ExternalLink className="h-4 w-4" />
                  </Button>
                )}
              </div>
            ))
          )}
        </div>
      </CardContent>
    </Card>
  );
}
