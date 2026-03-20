"use client"

import { useEffect } from "react"
import { useRouter, useSearchParams } from "next/navigation"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

type Tab = "dashboard" | "history" | "settings"

const DEFAULT_TAB: Tab = "dashboard"

export function DashboardTabs({ username }: { username: string }) {
  const router = useRouter()
  const searchParams = useSearchParams()
  const activeTab = (searchParams.get("tab") as Tab) ?? DEFAULT_TAB

  useEffect(() => {
    if (!searchParams.get("tab")) {
      const params = new URLSearchParams(searchParams.toString())
      params.set("tab", DEFAULT_TAB)
      router.replace(`?${params.toString()}`)
    }
  }, [])

  function handleTabChange(value: string) {
    const params = new URLSearchParams(searchParams.toString())
    params.set("tab", value)
    router.replace(`?${params.toString()}`)
  }

  console.log(username)
  return (
    <div className="w-full h-full pb-20">
      <Tabs value={activeTab} onValueChange={handleTabChange} className="w-full h-full">
        <TabsList variant="line" className="border-x border-b w-full *:cursor-pointer">
          <TabsTrigger value="dashboard" className="text-base">Dashboard</TabsTrigger>
          <TabsTrigger value="history" className="text-base">History</TabsTrigger>
          <TabsTrigger value="settings" className="text-base">Settings</TabsTrigger>
        </TabsList>
        <TabsContent value="dashboard">Make changes to your account here. <span className="text-sm text-muted-foreground">{username}</span></TabsContent>
        <TabsContent value="history">History here .</TabsContent>
        <TabsContent value="settings">Change your password here.</TabsContent>
      </Tabs>
    </div>
  )
}
