'use client';

import { useState } from 'react';
import { Layout } from '@/components/layout/Layout';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { assignmentsAPI } from '@/lib/api';
import useSWR from 'swr';
import { BookOpen, Clock, Award } from 'lucide-react';
import { formatDateTime } from '@/lib/utils';
import Link from 'next/link';

export default function AssignmentsPage() {
  const [statusFilter, setStatusFilter] = useState<string | undefined>();
  const [difficultyFilter, setDifficultyFilter] = useState<string | undefined>();

  const { data, isLoading } = useSWR(
    `/assignments?status=${statusFilter || ''}&difficulty=${difficultyFilter || ''}`,
    () =>
      assignmentsAPI.list({
        status: statusFilter,
        difficulty: difficultyFilter,
        limit: 50,
      }).then((res) => res.data)
  );

  const assignments = data || [];

  return (
    <Layout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">Assignments</h1>
            <p className="text-muted-foreground">
              Manage and solve your assignments with AI assistance
            </p>
          </div>
        </div>

        {/* Filters */}
        <div className="flex gap-4">
          <div className="flex gap-2">
            <Button
              variant={!statusFilter ? 'default' : 'outline'}
              size="sm"
              onClick={() => setStatusFilter(undefined)}
            >
              All
            </Button>
            <Button
              variant={statusFilter === 'pending' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setStatusFilter('pending')}
            >
              Pending
            </Button>
            <Button
              variant={statusFilter === 'completed' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setStatusFilter('completed')}
            >
              Completed
            </Button>
          </div>

          <div className="flex gap-2">
            <Button
              variant={difficultyFilter === 'easy' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setDifficultyFilter(difficultyFilter === 'easy' ? undefined : 'easy')}
            >
              Easy
            </Button>
            <Button
              variant={difficultyFilter === 'medium' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setDifficultyFilter(difficultyFilter === 'medium' ? undefined : 'medium')}
            >
              Medium
            </Button>
            <Button
              variant={difficultyFilter === 'hard' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setDifficultyFilter(difficultyFilter === 'hard' ? undefined : 'hard')}
            >
              Hard
            </Button>
          </div>
        </div>

        {/* Assignments List */}
        <div className="grid gap-4">
          {isLoading ? (
            <div className="text-center py-12 text-muted-foreground">Loading assignments...</div>
          ) : assignments.length === 0 ? (
            <div className="text-center py-12 text-muted-foreground">No assignments found</div>
          ) : (
            assignments.map((assignment: any) => (
              <Card key={assignment.hash} className="hover:shadow-md transition-shadow">
                <CardContent className="p-6">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <BookOpen className="h-5 w-5 text-blue-500" />
                        <h3 className="text-lg font-semibold">{assignment.title}</h3>
                        {assignment.difficulty && (
                          <span
                            className={`px-2 py-1 rounded-full text-xs font-medium ${
                              assignment.difficulty === 'easy'
                                ? 'bg-green-100 text-green-700'
                                : assignment.difficulty === 'medium'
                                ? 'bg-yellow-100 text-yellow-700'
                                : 'bg-red-100 text-red-700'
                            }`}
                          >
                            {assignment.difficulty}
                          </span>
                        )}
                        <span
                          className={`px-2 py-1 rounded-full text-xs font-medium ${
                            assignment.status === 'completed'
                              ? 'bg-green-100 text-green-700'
                              : 'bg-blue-100 text-blue-700'
                          }`}
                        >
                          {assignment.status}
                        </span>
                      </div>

                      <div className="flex items-center gap-6 text-sm text-muted-foreground">
                        {assignment.due_date && (
                          <div className="flex items-center gap-1">
                            <Clock className="h-4 w-4" />
                            Due: {formatDateTime(assignment.due_date)}
                          </div>
                        )}
                        <div>
                          Progress: {assignment.questions_solved}/{assignment.questions_total}
                        </div>
                        <div className="flex items-center gap-1">
                          <Award className="h-4 w-4 text-yellow-500" />
                          {assignment.xp} XP
                        </div>
                      </div>
                    </div>

                    <Link href={`/assignments/${assignment.hash}?course=${assignment.course_hash}`}>
                      <Button>
                        {assignment.status === 'completed' ? 'Review' : 'Solve'}
                      </Button>
                    </Link>
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </div>
      </div>
    </Layout>
  );
}
