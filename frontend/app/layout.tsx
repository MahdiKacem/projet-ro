import type { Metadata } from "next"
import { Inter } from "next/font/google"
import { ThemeProvider } from "@/components/theme-provider"
import "@/app/globals.css"
import { Toaster } from 'react-hot-toast';

const inter = Inter({
  subsets: ["latin"],
  display: 'swap',
  variable: '--font-inter'
})

export const metadata: Metadata = {
  title: {
    default: "Transportation Problem Solver",
    template: "%s | Transportation Solver"
  },
  description: "Optimize transportation costs between warehouses and clients",
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL || "http://localhost:3000"),
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
      <>
              <Toaster />
    <html lang="en" suppressHydrationWarning className={inter.variable}>
      <body className={`min-h-screen font-sans antialiased ${inter.className}`}>
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <main className="min-h-screen bg-background flex flex-col">
            {children}
          </main>
        </ThemeProvider>
      </body>
    </html>
      </>
  )
}