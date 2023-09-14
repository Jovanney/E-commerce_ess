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
      title: "ERROR!",
      description: "Produto inserido não é da mesma loja que os produtos do carrinho!",
      style: {
        backgroundColor: "#FF0000", // Cor vermelha para o fundo
        color: "white" // Cor branca para o texto
      },
    })
  }
}

function getImageByCategory(nome_prod: string): string {
  const defaultImage = "https://via.placeholder.com/150"; // Uma imagem padrão caso não haja correspondência

  const categoryImages: { [key: string]: string } = {
    'Monitor Hero III': "https://m.media-amazon.com/images/I/614wG7ko+yL._AC_UF894,1000_QL80_.jpg",
    'Camisa de Linho Capri Rosa': "https://br.puma.com/media/contentmanager/content/23AW_ECOM_MF_SP_The-Smurfs_FeatureHero_TabMob_Large_1536x1536_1.jpg",
    'Chuteira Puma HZA': "https://br.puma.com/media/contentmanager/content/23AW_Ecom_MF_TS_Football_Energy-Pack_FullBleedHero_Large_TabMob_1536x1536_Future.jpg",
    'Mochila Puma Redac': "https://images.puma.com/image/upload/f_auto,q_auto,b_rgb:fafafa/global/090030/01/fnd/BRA/w/640/h/640/fmt/png",
    'Carregador Iphone': "https://a-static.mlcdn.com.br/450x450/carregador-original-compativel-com-iphone-11-12-13-14-pro-max-usb-c-20w-fonte-turbo-novax/msveletronicos/6f3f4672cc9b11edbfa54201ac185033/a4d8f6376c5ec822ff891420d8bec034.jpeg",
    'Iphone 8': "https://www.estadao.com.br/resizer/WDaXgomLY76wo5RADSr6n9QQ-Y4=/arc-anglerfish-arc2-prod-estadao/public/7GUP6OC5NZLKTNQILBY7EKSORQ.jpg",
    'Iphone 13 pro max': "https://d8vlg9z1oftyc.cloudfront.net/ailos/image/product/9f332f23b834ef41ba5bddeaa1cffe3420220316144447/850/celular-apple-iphone-13-pro-max-128gb_3013.jpg",
    'Mouse RyzerX': "https://lojaibyte.vteximg.com.br/arquivos/ids/194133-1200-1200/mouse-gamer-razer-basilisk-essential-7-botoes-6400dpi-rz01-02650100-r3m1--1-.jpg?v=637306125465470000",
    'Camiseta Básica polo': "https://images.tcdn.com.br/img/img_prod/749496/camiseta_masculina_fio_egipcio_gola_u_preta_471_1_4af83b7404697eb4ebaeba5eed59618f.jpg"
  };

  return categoryImages[nome_prod] || defaultImage;
}

function Home() {
  const [produtos, setProdutos] = useState<Produto[]>([]);
  const isLoggedIn = !!localStorage.getItem('token'); // Verifique se o usuário está logado

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
            <div key={produto.id_produto} className="flex flex-col bg-white rounded-xl shadow-md overflow-hidden m-3 p-4 max-w-xs relative h-auto">
              
              <img 
                src={produto.imagem ? produto.imagem : getImageByCategory(produto.nome_produto)} 
                alt={produto.nome_produto} 
                className="w-full h-auto mb-4" 
              />

              <div className="flex-grow mb-2">{produto.descricao}</div>

              <div className="flex flex-col space-y-4 mt-auto"> 
                <div className="flex justify-between items-center">
                  <h2 className="text-lg font-bold">{produto.nome_produto}</h2>
                  <div className="font-semibold">R$ {produto.preco}</div>
                </div>

                {isLoggedIn && (
                  <Button
                    className='bg-navgreen'
                    type="submit"
                    variant="default"
                    size="default" 
                    onClick={() => addToCart(produto.id_produto)}
                  >
                    Comprar
                  </Button>
                )}
              </div>
              
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

export default Home;