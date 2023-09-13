import {
  GanttChartSquare,
  UserPlus
} from "lucide-react"

import { Button, buttonVariants } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import Link from "next/link"

export function DropdownMenuProduto() {
  return (
      <DropdownMenu>
          <DropdownMenuTrigger className={buttonVariants()}>Produtos&ensp;<GanttChartSquare size={30}/></DropdownMenuTrigger>
          <DropdownMenuContent>
              <DropdownMenuItem><Link href="/create">Adicionar Produto&ensp;</Link></DropdownMenuItem>
              <DropdownMenuItem><Link href="/update">Gerenciar Produtos&ensp;</Link></DropdownMenuItem>
              </DropdownMenuContent>
      </DropdownMenu>
  )
}
