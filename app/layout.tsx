import NavBar from '@/components/NavBar'
import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { Toaster } from '@/components/ui/toaster'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'E-PASS',
  description: 'E-pass',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="pt-br">
      <body className={inter.className}>
        <main className='h-screen flex flex-col justify-center items-center bg-bggray'> 
          <NavBar/>
          {children}
          <Toaster />
        </main>
      </body>
      
    </html>
  )
}
