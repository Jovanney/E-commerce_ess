"use client";

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { toast, useToast } from "@/components/ui/use-toast"

interface Produto {
  id_produto: number;
  nome_produto: string;
  descricao: string;
  preco: number;
  imagem: string;
  categoria_prod: string;  // supondo que você tenha imagens para os produtos
}

const DEFAULT_IMAGE_URL = "https://images.unsplash.com/photo-1560769629-975ec94e6a86?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1964&q=80";

const getProdutos = async (): Promise<Produto[]> => {  

  const res = await fetch(`http://127.0.0.1:8000/All_Produtos/`);

  if (!res.ok) {
    throw new Error(`Failed to fetch data: ${res.statusText}`);
  }
  
  const data = await res.json();
  return Array.isArray(data) ? data : [];
};

const addToCart = async (id_produto: number, quantidade: number = 1) => {
  const token = localStorage.getItem('token');

  if (!token) {
    console.error("Token não encontrado.");
    return;
  }

  try {
    const response = await fetch(`http://127.0.0.1:8000/novo-item/${id_produto}/${quantidade}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${JSON.parse(token)["access_token"]}`,
        'Content-Type': 'application/json'
      }
    });

    const result = await response.json();

    if (!response.ok) {
      console.error(result);
      throw new Error('Erro ao adicionar produto ao carrinho.');
    } else {
      // Aqui você pode adicionar algum feedback ao usuário, por exemplo:
      toast({
         title: "Produto adicionado ao carrinho!",
         description: "E-PASS",
         style: {
          backgroundColor: "#4CAF50", // Cor vermelha para o fundo
          color: "white" // Cor branca para o texto
        },
       })
    }

  } catch (error) {
    console.error(error);
    toast({
      title: "!ERROR!",
      description: "Produto inserido não é da mesma loja que os produtos do carrinho!",
      style: {
        backgroundColor: "#FF0000", // Cor vermelha para o fundo
        color: "white" // Cor branca para o texto
      },
    })
  }
}

function getImageByCategory(categoria_prod: string): string {
  const defaultImage = "https://via.placeholder.com/150"; // Uma imagem padrão caso não haja correspondência

  const categoryImages: { [key: string]: string } = {
    Eletronicos: "https://images.unsplash.com/photo-1608499296275-1f22c6391b88?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80",
    Vestuario: "https://images.unsplash.com/photo-1606316618796-2f57ce2398f3?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1974&q=80",
    Calçado: "https://images.unsplash.com/photo-1560769629-975ec94e6a86?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1964&q=80"
  };

  return categoryImages[categoria_prod] || defaultImage;
}

function Home() {
  const [produtos, setProdutos] = useState<Produto[]>([]);


  useEffect(() => {
    const fetchData = async () => {
      try {
        const produtosData = await getProdutos();
        setProdutos(produtosData);
      } catch (error) {
        console.error('Error fetching products:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="w-full min-h-screen bg-whitehistorico">
      <section className="container mx-auto mt-32">
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
          {produtos.map((produto) => (
            <div key={produto.id_produto} className="bg-white rounded-xl shadow-md overflow-hidden m-3 p-4">
              <img 
                src={produto.imagem ? produto.imagem : getImageByCategory(produto.categoria_prod)} 
                alt={produto.nome_produto} 
                className="w-full h-48 object-cover mb-4" 
              />

              <div className="flex justify-between items-center mb-2">
                <h2 className="text-lg font-bold">{produto.nome_produto}</h2>
                <div className="font-semibold">R$ {produto.preco}</div>
              </div>
            
              <div className="mb-2">{produto.descricao}</div>
              <Button
                className='bg-navgreen'
                type="submit"
                variant="default" // Defina a variante desejada
                size="default" 
                onClick={() => addToCart(produto.id_produto)}
              >
                Comprar
              </Button>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

export default Home;
