"use client";

import Link from 'next/link';
import { buttonVariants } from './ui/button';
import { CreditCard, GanttChartSquare, LogIn, ShoppingCart, Store, UserCog, UserPlus } from 'lucide-react';
import { useEffect, useState } from 'react';
import { DropdownMenuCreateUser } from './dropdownmenu/DropDownMenuCreateUser';
import { DropdownMenuConfigUser } from './dropdownmenu/DropDownMenuConfigUser';
import SearchBar from './SearchBar';
import { DropdownMenuProduto } from './dropdownmenu/DropDownMenuProduto';

interface cliente {
    cpf: string
    nome: string
    email: string
    senha: string
    admin: true
    enderecos: []
    telefones: []
    pedidos: []
}

const NavBar: React.FC = () => {
  const [cliente, setCliente] = useState<cliente>();
  const [loja, setLoja] = useState(false);

  useEffect(() => {
    const getCurrentUser = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const response = await fetch('http://127.0.0.1:8000/users/me', {
            headers: {
              'Authorization': `Bearer ${JSON.parse(token)["access_token"]}`
            }
          });
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          const user = await response.json();
          if (user.cpf != null) {
            setCliente(user);
          }
          else {
            setLoja(user);
          }
        } catch (error) {
          console.log(error);
        }
      } 
    }
    getCurrentUser();
  }, []);

  return (
    <nav className="bg-navgreen p-4 fixed w-full z-10 top-0 border-b-2 border-bluebord">
      <div className="flex gap-x-16">
        <div className='flex gap-3 items-center w-full'>
          <Link href="/" className={buttonVariants()}>E-PASS&ensp;<Store size={30} /></Link>
        </div>
        <div className='w-full'><SearchBar/></div>

        {cliente ? (
          <div className='flex gap-3 items-center justify-end w-full'>
            <DropdownMenuConfigUser/>
            <Link href="/" className={buttonVariants()}>Carrinho&ensp;<ShoppingCart size={30}/></Link>
            <Link href="/" className={buttonVariants()}>Pedidos&ensp;<CreditCard size={30}/></Link>
          </div>
        ) : loja ? (
          <div className='flex gap-3 items-center justify-end w-full'>
            <DropdownMenuConfigUser/>
            <DropdownMenuProduto/>
          </div>
        )
        : (
          <div className='flex gap-3 items-center justify-end w-full'>
            <DropdownMenuCreateUser/>
            <Link href="/sign-in" className={buttonVariants()}>Login&ensp;<LogIn size={20}/> </Link>
          </div>
        )}
          
      </div>
    </nav>
  );
};

export default NavBar;
