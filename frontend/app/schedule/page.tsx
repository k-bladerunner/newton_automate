'use client';

import { Layout } from '@/components/layout/Layout';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { scheduleAPI } from '@/lib/api';
import useSWR from 'swr';
import { Calendar, Clock, MapPin, ExternalLink, User } from 'lucide-react';
import { formatTime, getTimeUntil } from '@/lib/utils';

export default function SchedulePage() {
  const { data: todaySchedule, isLoading: loadingToday } = useSWR('/schedule/today', () =>
    scheduleAPI.today().then((res) => res.data)
  );

  const { data: weekSchedule, isLoading: loadingWeek } = useSWR('/schedule/week', () =>
    scheduleAPI.week().then((res) => res.data)
  );

  const today = todaySchedule || [];
  const week = weekSchedule || [];

  const handleJoinClass = async (lectureSlotHash: string, joinUrl: string) => {
    if (joinUrl) {
      window.open(joinUrl, '_blank');
    }
  };

  // Group week schedule by date
  const groupedByDate = week.reduce((acc: any, classItem: any) => {
    const date = new Date(classItem.start_timestamp * 1000).toLocaleDateString();
    if (!acc[date]) acc[date] = [];
    acc[date].push(classItem);
    return acc;
  }, {});

  return (
    <Layout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold">Schedule</h1>
          <p className="text-muted-foreground">
            View your class schedule and join sessions
          </p>
        </div>

        {/* Today's Schedule */}
        <div>
          <h2 className="text-2xl font-semibold mb-4">Today's Classes</h2>
          {loadingToday ? (
            <div className="text-center py-12 text-muted-foreground">Loading...</div>
          ) : today.length === 0 ? (
            <Card>
              <CardContent className="py-12 text-center text-muted-foreground">
                No classes scheduled for today
              </CardContent>
            </Card>
          ) : (
            <div className="grid gap-4">
              {today.map((classItem: any) => (
                <Card key={classItem.hash} className="hover:shadow-md transition-shadow">
                  <CardContent className="p-6">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <h3 className="text-lg font-semibold mb-2">{classItem.subject}</h3>

                        <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
                          <div className="flex items-center gap-1">
                            <Clock className="h-4 w-4" />
                            {formatTime(classItem.start_timestamp)} -{' '}
                            {formatTime(classItem.end_timestamp)}
                          </div>

                          {classItem.room && (
                            <div className="flex items-center gap-1">
                              <MapPin className="h-4 w-4" />
                              {classItem.room}
                            </div>
                          )}

                          {classItem.instructor && (
                            <div className="flex items-center gap-1">
                              <User className="h-4 w-4" />
                              {classItem.instructor}
                            </div>
                          )}
                        </div>

                        <div className="mt-2 text-sm font-medium text-blue-600">
                          {getTimeUntil(classItem.start_timestamp)}
                        </div>
                      </div>

                      {classItem.join_url && (
                        <Button
                          onClick={() => handleJoinClass(classItem.hash, classItem.join_url)}
                        >
                          <ExternalLink className="h-4 w-4 mr-2" />
                          Join Class
                        </Button>
                      )}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>

        {/* Week Schedule */}
        <div>
          <h2 className="text-2xl font-semibold mb-4">This Week</h2>
          {loadingWeek ? (
            <div className="text-center py-12 text-muted-foreground">Loading...</div>
          ) : Object.keys(groupedByDate).length === 0 ? (
            <Card>
              <CardContent className="py-12 text-center text-muted-foreground">
                No classes scheduled for this week
              </CardContent>
            </Card>
          ) : (
            <div className="space-y-6">
              {Object.entries(groupedByDate).map(([date, classes]: [string, any]) => (
                <div key={date}>
                  <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                    <Calendar className="h-5 w-5" />
                    {date}
                  </h3>
                  <div className="grid gap-3">
                    {classes.map((classItem: any) => (
                      <Card key={classItem.hash}>
                        <CardContent className="p-4">
                          <div className="flex items-center justify-between">
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
                            </div>
                            {classItem.join_url && (
                              <Button
                                size="sm"
                                variant="outline"
                                onClick={() => handleJoinClass(classItem.hash, classItem.join_url)}
                              >
                                <ExternalLink className="h-4 w-4" />
                              </Button>
                            )}
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}
