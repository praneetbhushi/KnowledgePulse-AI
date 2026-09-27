interface StatCardProps {
  title: string;
  value: string;
  subtitle?: string;
}

export default function StatCard({
  title,
  value,
  subtitle,
}: StatCardProps) {
  return (
    <div className="rounded-xl bg-white p-6 shadow border">
      <h3 className="text-gray-500 text-sm">{title}</h3>

      <p className="mt-3 text-4xl font-bold">
        {value}
      </p>

      {subtitle && (
        <p className="mt-2 text-sm text-gray-500">
          {subtitle}
        </p>
      )}
    </div>
  );
}