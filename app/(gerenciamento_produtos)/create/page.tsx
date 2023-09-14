"use client";
import NavBar from '@/components/NavBar';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import React, { useState } from 'react';
import { toast, useToast } from "@/components/ui/use-toast"
import { PanelTopInactive } from 'lucide-react';


interface ItemBase {
  // Defina os campos de ItemBase aqui, se necessário
}

interface ProdutoCreate {
  id_produto: number;
  cnpj_loja: string;
  categoria_prod: string;
  nome_produto: string;
  marca_produto: string;
  preco: string;
  especificacoes: string;
  itens: ItemBase[];
}

const addProduto = async (newProduto: ProdutoCreate) => {
  const token = localStorage.getItem('token');
  if(token){
  try {
    const response = await fetch(`http://127.0.0.1:8000/add_produtos/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${JSON.parse(token)["access_token"]}`
      },
      body: JSON.stringify(newProduto),
    });

    if (response.ok) {
      toast({
        title: "Produto criado com Sucesso!",
        description: "E-PASS",
        style: {
          backgroundColor: "#4CAF50", 
          color: "white" 
        }
      });
    } else {
      toast({
        title: "Error adding product",
        description: "E-PASS",
        style: {
          backgroundColor: "#FF0000", 
          color: "white" 
        }
      });
    }
  } catch (error) {
    toast({
      title: "Error adding product",
      description: "E-PASS",
      style: {
        backgroundColor: "#FF0000", 
        color: "white" 
      }
    });
  }
}
};

function AddProduto() {
  const [newProduto, setNewProduto] = useState<ProdutoCreate>({
    id_produto: 0,
    cnpj_loja: '',
    categoria_prod: '',
    nome_produto: '',
    marca_produto: '',
    preco: '',
    especificacoes: '',
    itens: [],
  });

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    try {
      await addProduto(newProduto);
      setNewProduto({
        id_produto: 0,
        cnpj_loja: '',
        categoria_prod: '',
        nome_produto: '',
        marca_produto: '',
        preco: '',
        especificacoes: '',
        itens: [],
      });
    } catch (error) {
      toast({
        title: "Error adding product",
        description: "E-PASS",
        style: {
          backgroundColor: "#FF0000", 
          color: "white" 
        }
      });
    }
  };

  return (
    <div className="flex flex-col items-center w-full items-center min-h-screen bg-whitehistorico">
      <NavBar/> 
      <div className="flex-1 text-center bg-whitehistorico p-2 pt-60">
        <div className="p-4">
          <div className="bg-white shadow-md p-6 mb-6 justify-between border border-black border-2 rounded">
          <h1 className="mb-4 text-2xl"><div className="flex flex-row"><PanelTopInactive /><b> Cadastro de produto</b></div></h1>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="">
                <Label className="block">
                  Categoria do Produto:
                  <Input
                    type="text"
                    value={newProduto.categoria_prod}
                    onChange={(event) =>
                      setNewProduto({
                        ...newProduto,
                        categoria_prod: event.target.value,
                      })
                    }
                    className="px-2 py-1 border rounded-md"
                  />
                </Label>
              </div>
              <div>
                <Label className="block">
                  Nome do Produto:
                  <Input
                    type="text"
                    value={newProduto.nome_produto}
                    onChange={(event) =>
                      setNewProduto({
                        ...newProduto,
                        nome_produto: event.target.value,
                      })
                    }
                    className="px-2 py-1 border rounded-md"
                  />
                </Label>
              </div>
              <div>
                <Label className="block">
                  Marca do Produto:
                  <Input
                    type="text"
                    value={newProduto.marca_produto}
                    onChange={(event) =>
                      setNewProduto({
                        ...newProduto,
                        marca_produto: event.target.value,
                      })
                    }
                    className="px-2 py-1 border rounded-md"
                  />
                </Label>
              </div>
              <div>
                <Label className="block">
                  Preço do Produto:
                  <Input
                    type="text"
                    value={newProduto.preco}
                    onChange={(event) =>
                      setNewProduto({
                        ...newProduto,
                        preco: event.target.value,
                      })
                    }
                    className="px-2 py-1 border rounded-md"
                  />
                </Label>
              </div>
              <div>
                <Label className="block">
                  Especificações do Produto:
                  <Input
                    type="text"
                    value={newProduto.especificacoes}
                    onChange={(event) =>
                      setNewProduto({
                        ...newProduto,
                        especificacoes: event.target.value,
                      })
                    }
                    className="px-2 py-1 border rounded-md"
                  />
                </Label>
              </div>
              <div className="text-right">
                <Button
                  className='bg-green-success'
                  type="submit"
                  variant="default"
                  size="default" 
                >
                  Cadastrar
                </Button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AddProduto;