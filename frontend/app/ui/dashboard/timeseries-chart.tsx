'use client';

import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from 'recharts';

type Point = {
  ts: string;
  value: number;
};

const dateRangeMap: Record<string, Intl.DateTimeFormatOptions> = {
  day: {
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
  },
  week: {
    weekday: 'short',
  },

  month: {
    day: 'numeric',
    month: 'numeric',
  },

  year: {
    month: 'short',
  },
};

export default function TimeSeriesChart({
  data,
  range,
}: {
  data: Point[];
  range: 'day' | 'month' | 'week' | 'year';
}) {
  const formatter = new Intl.DateTimeFormat('fi-FI', {
    ...dateRangeMap[range],
    timeZone: 'Europe/Helsinki',
  });

  const formatted = data.map((d) => ({
    ...d,
    time: formatter.format(new Date(d.ts)),
  }));

  return (
    <AreaChart
      style={{ width: '100%', aspectRatio: 1.618 }}
      responsive
      data={formatted}
      margin={{ top: 10, right: 0, left: 0, bottom: 0 }}
    >
      <defs>
        <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
          <stop offset="5%" stopColor="#73db9a" stopOpacity={0.5} />
          <stop offset="95%" stopColor="#73db9a" stopOpacity={0} />
        </linearGradient>
      </defs>

      <CartesianGrid stroke="rgba(255,255,255,0.05)" vertical={false} horizontal={false} />

      <XAxis
        dataKey="time"
        tick={{ fill: '#888', fontSize: 12 }}
        axisLine={false}
        tickLine={false}
      />

      <YAxis
        orientation="right"
        tick={{ fill: '#888', fontSize: 12 }}
        axisLine={false}
        tickLine={false}
        width={'auto'}
        domain={['auto', 'auto']}
      />

      <Tooltip
        contentStyle={{
          background: '#111',
          border: '1px solid #222',
          borderRadius: '12px',
        }}
        labelStyle={{ color: '#aaa' }}
      />

      <Area
        type="monotone"
        dataKey="value"
        stroke="#73db9a"
        strokeWidth={2.5}
        fill="url(#colorValue)"
        dot={false}
        activeDot={{ r: 6, strokeWidth: 5, strokeOpacity: 0.1 }}
      />
    </AreaChart>
  );
}
