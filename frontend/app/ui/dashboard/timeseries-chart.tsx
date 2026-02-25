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

export default function TimeSeriesChart({ data }: { data: Point[] }) {
  const formatted = data.map((d) => ({
    ...d,
    time: new Date(d.ts).toLocaleTimeString([], {
      hour: '2-digit',
      minute: '2-digit',
    }),
  }));

  return (
    <div className="h-64 w-full">
      <ResponsiveContainer>
        <AreaChart data={formatted}>
          <defs>
            <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#FA5C5C" stopOpacity={0.35} />
              <stop offset="95%" stopColor="#FA5C5C" stopOpacity={0} />
            </linearGradient>
          </defs>

          <CartesianGrid stroke="rgba(255,255,255,0.05)" vertical={false} />

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
            stroke="#ffffff"
            strokeWidth={2}
            fill="url(#colorValue)"
            dot={false}
            activeDot={{ r: 6 }}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
