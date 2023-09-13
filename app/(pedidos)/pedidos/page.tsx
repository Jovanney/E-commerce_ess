"use client";

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import {toast, useToast} from "@/components/ui/use-toast";


interface Item {
  quantidade: number;
  nome_produto: string;
}

interface PedidoData {
  id_pedido: number;
  preco_total: number;
  itens: Item[];
  id_status: number;
  message?: string; // Novo campo
}

const getPedidos = async () => {  
  const token = localStorage.getItem('token');
  if (!token) {
    throw new Error("Token não encontrado.");
  }
  
  const res = await fetch(`http://127.0.0.1:8000/pedidos`, {
    headers: {
        'Authorization': `Bearer ${JSON.parse(token)["access_token"]}`
      }
  });
  if (!res.ok) {
    throw new Error(`Failed to fetch data: ${res.statusText}`);
  }
  
  const data = await res.json();

  if (data.length === 1 && data[0].mensagem) {
    return { mensagem: data[0].mensagem };
  }

  return Array.isArray(data) ? data : [];
};

const cancelPedido = async (id_pedido: number) => {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error("Token não encontrado.");
    }
  
    const res = await fetch(`http://127.0.0.1:8000/cancelar_pedido/${id_pedido}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${JSON.parse(token)["access_token"]}`
      }
    });
    
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail);
    }
    return data;
  };

const STATUS_MAP: { [key: number]: string } = {
  1: "Não confirmado",
  2: "Confirmado",
  3: "Em rota",
  4: "Concluído",
  5: "Cancelado"
};

function PedidoList() {
  useToast();
  const [pedidos, setPedidos] = useState<PedidoData[] | { mensagem: string } | null>(null);


  useEffect(() => {
    // Função para buscar pedidos ao montar o componente
    const fetchData = async () => {
      try {
        const pedidosData = await getPedidos();
        setPedidos(pedidosData);
      } catch (error: any) {
        console.error('Error fetching data:', error);
        // Aqui, definimos a mensagem de erro no pedido correspondente
      }
    };

    fetchData();
  }, []);

  const handleCancel = async (id_pedido: number) => {
    try {
      await cancelPedido(id_pedido);
      setPedidos((prev) =>
        prev?.map((pedido: { id_pedido: number; }) =>
          pedido.id_pedido === id_pedido
            ? { ...pedido, message: "", id_status: 5 } // Atualizar o status para 'Cancelado' aqui
            : pedido
        )
      );

      toast({
        title: "Cancelado",
        description: "Pedido cancelado com sucesso.",
        style: {
          backgroundColor: "#4CAF50",
          color: "white"
        }
      });


      // Limpar a mensagem após 5 segundos
    } catch (error: any) {

      if (error.response?.status === 403) {
        toast({
          title: "Erro ao cancelar pedido!",
          description: "Pedido não pode mais ser cancelado.",
          style: {
            backgroundColor: "#FF0000", // Cor vermelha para o fundo
            color: "white" // Cor branca para o texto
          }
        });
      } else {
        toast({
          title: "Erro ao cancelar pedido!",
          description: "Pedido já saiu para entrega. Não pode mais ser cancelado",
          style: {
            backgroundColor: "#FF0000", // Cor vermelha para o fundo
            color: "white" // Cor branca para o texto
          }
        });
      }
    }
  };
    

  
  return (
    <div className="w-full min-h-screen bg-whitehistorico">
      <section className="container mx-auto mt-32">
        {
          pedidos === null ? 
          <div className="max-w-xl mx-auto bg-white rounded-xl shadow-md overflow-hidden m-3 p-4 text-center">
            Carregando...
          </div>
          :
          Array.isArray(pedidos) ? 
            (pedidos as PedidoData[]).map((pedido) => (
              <div key={pedido.id_pedido} className="max-w-xl mx-auto bg-white rounded-xl shadow-md overflow-hidden m-3 p-4">
                {pedido.message && (
                  <div className={`mb-4 text-center ${pedido.message === "Pedido cancelado com sucesso" ? "text-green-success" : "text-red-info"}`}>
                    {pedido.message}
                  </div>
                )}
                <h2 className="text-lg font-bold mb-4">Informações do Pedido</h2>
                <div className="mb-4">
                    <strong>ID Pedido:</strong> {pedido.id_pedido}
                </div>
                <div className="mb-4">
                    <strong>Preço Total:</strong> R$ {pedido.preco_total.toFixed(2)}
                </div>
                <div className="mb-4">
                    <strong>Status:</strong> {STATUS_MAP[pedido.id_status]}
                </div>
                <h3 className="text-md font-semibold mb-2">Itens do Pedido:</h3>
                <ul>
                    {pedido.itens.map((item, idx) => (
                        <li key={idx} className="mb-2">
                            {item.quantidade}x {item.nome_produto}
                        </li>
                    ))}
                </ul>
  
                {(pedido.id_status === 5) ? (
                    <div className="mt-4 bg-red-light text-white px-4 py-2 rounded text-center">
                        Pedido cancelado
                    </div>
                ) : (
                    (pedido.id_status === 2 || pedido.id_status === 3 || pedido.id_status === 4) && (
                        <Button 
                            variant="destructive"
                            onClick={() => handleCancel(pedido.id_pedido)}
                        >
                            Cancelar Pedido
                        </Button>
                    )
                )}
              </div>
            ))
          :
            'mensagem' in pedidos ? 
              <div className="max-w-xl mx-auto bg-white rounded-xl shadow-md overflow-hidden m-3 p-4 text-center">
                {pedidos.mensagem}
              </div>
            :
            null
        }
      </section>
    </div>
  );
  

  
}
  
export default PedidoList; 