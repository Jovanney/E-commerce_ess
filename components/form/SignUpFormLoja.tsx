'use client';

import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "../ui/form";
import * as z from "zod"
import { useForm } from "react-hook-form"
import { Input } from "../ui/input";
import { Button } from "../ui/button";
import { zodResolver} from "@hookform/resolvers/zod"
import Link from "next/link";

const FormSchema = z.object({
    cnpj: z.string().min(1, 'É necessário informar um cnpj').max(14, 'Cnpj deve conter de 14 dígitos'),
    email: z.string().min(1, 'É necessário informar o E-mail').email('Email Inválido'),
    senha: z.string().min(1, 'É necessário informar a senha').min(8, 'Senha deve ter mais de 8 caracteres'),
    confirmarsenha: z.string().min(1, 'É necessário informar a confirmação da senha').min(8, 'Senha deve ter mais de 8 caracteres'),
    nome: z.string().min(1, 'É necessário informar um nome de tamanho válido'),
})
.refine((data) => data.senha === data.confirmarsenha, {
    path: ['confirmarsenha'],
    message: 'As senhas não são iguais'
})

const onSubmit = async (values: z.infer<typeof FormSchema>) => {
    const response = await fetch(`http://127.0.0.1:8000/loja/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'cnpj': values.cnpj,
            'nome': values.nome,
            'email': values.email,
            'senha': values.senha
        })
    })
    if (!response.ok) {
        console.log(response);
      }
    else {
        window.location.href= '/'
    }
};



const SignUpFormLoja = () => {
    const form = useForm<z.infer<typeof FormSchema>>({
        resolver: zodResolver(FormSchema),
      })
      
    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="w-full">
                <div className="space-y-2">
                    <FormField
                    control={form.control}
                    name="email"
                    render={({ field }) => (
                        <FormItem>
                        <FormLabel>Email</FormLabel>
                        <FormControl>
                            <Input placeholder="exemplo@gmail.com" type="email" {...field} />
                        </FormControl>
                        <FormMessage />
                        </FormItem>
                    )}
                    />
                    <FormField
                    control={form.control}
                    name="senha"
                    render={({ field }) => (
                        <FormItem>
                        <FormLabel>Senha</FormLabel>
                        <FormControl>
                            <Input placeholder="senha..." type="password" {...field} />
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
                        <FormLabel>Re-escrever Senha</FormLabel>
                        <FormControl>
                            <Input placeholder="senha..." type="password" {...field} />
                        </FormControl>
                        <FormMessage />
                        </FormItem>
                    )}
                    />
                    <FormField
                    control={form.control}
                    name="cnpj"
                    render={({ field }) => (
                        <FormItem>
                        <FormLabel>Cnpj</FormLabel>
                        <FormControl>
                            <Input placeholder="123456789101112" type="text" {...field} />
                        </FormControl>
                        <FormMessage />
                        </FormItem>
                    )}
                    />
                    <FormField
                    control={form.control}
                    name="nome"
                    render={({ field }) => (
                        <FormItem>
                        <FormLabel>Nome</FormLabel>
                        <FormControl>
                            <Input placeholder="Fornecedor Ata" type="text" {...field} />
                        </FormControl>
                        <FormMessage />
                        </FormItem>
                    )}
                    />
                </div>

        <Button className="w-full mt-6" type="submit">Criar Conta</Button>
      </form>
      {/* <div className="mx-auto my-4 flex w-full items-center justify-evenly before:mr-4 before:block before:h-px before:flex-grow
      before:bg-stone-400 after:ml-4 after:h-px after:block after:flex-grow after:bg-stone-400">
        Ou 
      </div>
      <p className="text-center text-sm text-gray-600 mt-2">
         Caso já possua conta, então você pode&nbsp;  
        <Link className="text-blue-500 underline" href='/sign-in'>logar</Link>
      </p> */}
    </Form>
    )

};

export default SignUpFormLoja;

