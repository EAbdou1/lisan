import { currentUser } from "@clerk/nextjs/server";
import { DashboardTabs } from "../../components/dashboard-tabs"
import { redirect } from "next/navigation";
import { ClerkLoaded, Show } from "@clerk/nextjs";

export default async function DashboardPage() {
  const user = await currentUser();
  if (!user) {
    redirect("/sign-in");
  }
  return <ClerkLoaded><Show when={'signed-in'}> <DashboardTabs username={user.fullName ?? user.username ?? ""} /></Show></ClerkLoaded>
}
