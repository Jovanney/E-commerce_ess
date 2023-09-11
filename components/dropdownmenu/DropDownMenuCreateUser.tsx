import {
    UserPlus
  } from "lucide-react"
  
  import { Button, buttonVariants } from "@/components/ui/button"
  import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
  } from "@/components/ui/dropdown-menu"
import Link from "next/link"
  
  export function DropdownMenuCreateUser() {
    return (
        <DropdownMenu>
            <DropdownMenuTrigger className={buttonVariants()}>Cadastrar-se&ensp;<UserPlus size={30}/></DropdownMenuTrigger>
            <DropdownMenuContent>
                <DropdownMenuLabel>Eu Sou:</DropdownMenuLabel>
                <DropdownMenuSeparator/>
                <DropdownMenuItem><Link href="/sign-up-cliente">Cliente</Link></DropdownMenuItem>
                <DropdownMenuItem><Link href="/sign-up-loja">Loja</Link></DropdownMenuItem>
                </DropdownMenuContent>
        </DropdownMenu>
    )
  }
  