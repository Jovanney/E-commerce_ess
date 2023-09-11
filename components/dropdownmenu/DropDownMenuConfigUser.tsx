import {
  UserCog,
} from "lucide-react"

import { Button, buttonVariants } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "../ui/form";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { useCallback } from "react";
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger } from "../ui/alert-dialog"
import { Input } from "../ui/input";
import * as z from "zod";
import { zodResolver} from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";

const FormSchema = z.object({
    senha: z.string().min(1, 'É necessário informar a senha antiga'),
    novaSenha: z.string().min(1, 'É necessário informar a nova senha'),
    confirmarsenha: z.string().min(1, 'É necessário informar a nova senha')
})
.refine((data) => data.novaSenha === data.confirmarsenha, {
    path: ['confirmarsenha'],
    message: 'As senhas não são iguais'
});


const changePassword = async (values: z.infer<typeof FormSchema>) => {
  const token = localStorage.getItem('token');
  if (token) {
    const url = new URL(`http://127.0.0.1:8000/usuario/update_senha`);
    url.searchParams.append('old_password', values.senha);
    url.searchParams.append('new_password', values.novaSenha);
    const response = await fetch(url, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${JSON.parse(token)["access_token"]}`
      },
      body: JSON.stringify({
        old_password: values.senha,
        new_password: values.novaSenha
      })
    })
    if (!response.ok) {
      alert("Senha antiga incorreta");
    }
    else {
      window.location.href= '/'
    }
  }
};

const onLogout = () => {
  localStorage.removeItem('token');
  window.location.href= '/';
};

const deleteAccount = async () => {
  const token = localStorage.getItem('token');
  if (token) {
    try {
      const response = await fetch('http://127.0.0.1:8000/usuario/delete', {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${JSON.parse(token)["access_token"]}`
        }
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      else {
        localStorage.removeItem('token');
        window.location.href= '/';
      }
    } catch (error) {
      console.log(error);
    }
  } 
};

export function DropdownMenuConfigUser() {

  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
  })
  return (
    <Dialog>
      <AlertDialog>
        <DropdownMenu>
          <DropdownMenuTrigger className={buttonVariants()}>Conta&ensp;<UserCog size={30}/></DropdownMenuTrigger>
          <DropdownMenuContent>
            <DialogTrigger asChild>
              <DropdownMenuItem><button>Alterar Senha</button></DropdownMenuItem>
            </DialogTrigger>
            <DropdownMenuItem><button onClick={onLogout}>Deslogar</button></DropdownMenuItem>
            <AlertDialogTrigger>
                <DropdownMenuItem><button>Apagar conta</button></DropdownMenuItem>  
            </AlertDialogTrigger>
          </DropdownMenuContent>
        </DropdownMenu>
        <DialogContent className="sm:max-w-[550px]">
          <DialogHeader>
            <DialogTitle>Alterar senha</DialogTitle>
            <DialogDescription>
              Altere sua senha aqui, clique em salvar quando terminar
            </DialogDescription>
          </DialogHeader>
            <Form {...form}>
              <form onSubmit={form.handleSubmit(changePassword)} className="w-full">
                <div className="space-y-2">
                    <FormField
                    control={form.control}
                    name="senha"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Senha Antiga</FormLabel>
                            <FormControl>
                                <Input placeholder="senha antiga..." type="password" {...field} />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                    />
                    <FormField
                    control={form.control}
                    name="novaSenha"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Nova Senha</FormLabel>
                            <FormControl>
                                <Input placeholder=" nova senha..." type="password" {...field} />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                    />
                    <FormField
                    control={form.control}
                    name="confirmarsenha"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Confirme a nova Senha</FormLabel>
                            <FormControl>
                                <Input placeholder="confirme a nova senha..." type="password" {...field} />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                    />
                </div>

                <Button className="w-full mt-6" type="submit">Salvar</Button>
              </form>
            </Form>
        </DialogContent>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Você tem certeza absoluta?</AlertDialogTitle>
            <AlertDialogDescription>
                Essa ação não pode ser desfeita. Você tem certeza que quer apagar essa conta permanentemente
                dos nossos servidores?
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancelar</AlertDialogCancel>
            <AlertDialogAction onClick={deleteAccount}>Confirmar</AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </Dialog>


  )
}
