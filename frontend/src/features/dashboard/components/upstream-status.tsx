import { useQuery } from "@tanstack/react-query";
import { Activity, Globe, ShieldCheck } from "lucide-react";

import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";

export function UpstreamStatus() {
  const { data, isLoading } = useQuery({
    queryKey: ["health", "upstream"],
    queryFn: async () => {
      const resp = await fetch("/health/upstream");
      if (!resp.ok) throw new Error("Failed to fetch upstream status");
      return resp.json();
    },
    refetchInterval: 30000,
  });

  if (isLoading || !data) return null;

  return (
    <Card className="overflow-hidden border-primary/10 bg-primary/5">
      <CardContent className="p-4">
        <div className="flex flex-wrap items-center gap-x-6 gap-y-3">
          <div className="flex items-center gap-2.5">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10">
              <Globe className="h-4 w-4 text-primary" />
            </div>
            <div>
              <p className="text-[10px] font-medium uppercase tracking-wider text-muted-foreground">Upstream URL</p>
              <p className="text-sm font-semibold tracking-tight">{data.upstream_url}</p>
            </div>
          </div>

          <div className="flex items-center gap-2.5">
            <div className={cn(
              "flex h-8 w-8 items-center justify-center rounded-lg",
              data.is_openai_compatible ? "bg-emerald-500/10" : "bg-blue-500/10"
            )}>
              <Activity className={cn(
                "h-4 w-4",
                data.is_openai_compatible ? "text-emerald-500" : "text-blue-500"
              )} />
            </div>
            <div>
              <p className="text-[10px] font-medium uppercase tracking-wider text-muted-foreground">Protocol</p>
              <p className="text-sm font-semibold tracking-tight">
                {data.is_openai_compatible ? "OpenAI Compatible" : "Internal Responses"}
              </p>
            </div>
          </div>

          {data.anthropic_compatibility && (
            <div className="flex items-center gap-2.5">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-amber-500/10">
                <ShieldCheck className="h-4 w-4 text-amber-500" />
              </div>
              <div>
                <p className="text-[10px] font-medium uppercase tracking-wider text-muted-foreground">Anthropic Bridge</p>
                <p className="text-sm font-semibold tracking-tight">Active (v1/messages)</p>
              </div>
            </div>
          )}

          <div className="ml-auto flex items-center gap-2 rounded-full border border-emerald-500/20 bg-emerald-500/5 px-2.5 py-1">
            <div className="h-1.5 w-1.5 animate-pulse rounded-full bg-emerald-500" />
            <span className="text-[10px] font-medium text-emerald-600 dark:text-emerald-400">LIVE</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
