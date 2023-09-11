'use client';

import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "../ui/form";
import * as z from "zod"
import { useForm } from "react-hook-form"
import { Input } from "../ui/input";
import { Button } from "../ui/button";
import { zodResolver} from "@hookform/resolvers/zod"
import Link from "next/link";

const FormSchema = z.object({
    email: z.string().min(1, 'É necessário informar o E-mail').email('Email Inválido'),
    senha: z.string().min(1, 'É necessário informar a senha').min(8, 'Senha deve ter mais de 8 caracteres'),
})

const onSubmit = async (values: z.infer<typeof FormSchema>) => {
    const response = await fetch(`http://127.0.0.1:8000/token`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            'username': values.email,
            'password': values.senha
        })
    })
    if (!response.ok) {
        alert('Usuário ou Senha Incorretos');
      }
    else {
        const token = await response.json()
        localStorage.setItem("token", JSON.stringify(token))
        window.location.href= '/'
    }
};


const SignInForm = () => {
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
                        <FormDescription>
                            Informe o seu e-mail
                        </FormDescription>
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
                        <FormDescription>
                            Informe sua senha
                        </FormDescription>
                        <FormMessage />
                        </FormItem>
                    )}
                    />
                </div>

        <Button className="w-full mt-6" type="submit">Logar</Button>
      </form>
    </Form>
    
        )

};

export default SignInForm;

