import Navbar from '@/components/navigation/navbar'
import React from 'react'

export default function layout({ children }: { children: React.ReactNode }) {
  return (

    <div className='w-full'>
      <main className=" min-h-full flex flex-col max-w-5xl mx-auto">  <Navbar />
        <div className=''>
          {children}</div> </main>
    </div>
  )
}
