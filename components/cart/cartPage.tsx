"use client"
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Input} from '@/components/ui/input';
import {
  Table,
  TableBody,
  TableCell,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Minus, Plus, ShoppingBag, Trash2 } from 'lucide-react';


import React, { useEffect, useState } from 'react';

const cartPage = () => {
  interface Item {
    id: string;
    nome_produto: string;
    preco: string;
    quantidade: number;
  }

  const [items, setItems] = useState<Item[]>([]);
  const DEFAULT_IMAGE_URL = "https://cdn.discordapp.com/attachments/1024735926557089812/1151889989731369001/shopping-cart_icon-icons.png";

  useEffect(() => {
    const fetchData = async () => {
      const token = localStorage.getItem('token');
      if (token) {
  
      try {
        const res = await fetch(`http://127.0.0.1:8000/my-cart/`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${JSON.parse(token)["access_token"]}`
          },
        });
        const data = await res.json();

        setItems(data);
        console.log(data);
      } catch (error) {
        console.error('Erro ao buscar dados:', error);
      }
    }
    };

    fetchData();
  }, []);

  const clearCart = async () => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const res = await fetch(`http://127.0.0.1:8000/clear-carrinho/`, { method: 'DELETE', 
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${JSON.parse(token)["access_token"]}`
        }
      });
        const data = await res.json();
        setItems([]);
      } catch (error) {
        console.error('Erro ao limpar carrinho:', error);
      }
    };
  };

  const incrementQuantity = async (id_produto: string) => {
    const token = localStorage.getItem('token');
    if (token) {
  
    try {
      const response = await fetch(`http://127.0.0.1:8000/novo-item/${id_produto}/${1}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${JSON.parse(token)["access_token"]}`
        },
        body: JSON.stringify({
        }),
      });

      if (response.ok) {
        const updatedProduct = await response.json();
        console.log('Resposta do back-end após o primeiro clique:', updatedProduct);
        const updatedItems = items.map(item => {
          if (item.id === updatedProduct.id_produto) {
            return { ...item, quantidade: updatedProduct.quantidade};
          }
          return item;
        });

        setItems(updatedItems);
      } else {
        console.error('Erro ao incrementar o item:', await response.text());
      }
      } catch (error) {
        console.error('Erro ao adicionar quantidade ao carrinho:', error);
      }
    }
  };

  const reduceQuantity = async (id_produto: string) => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const res = await fetch(`http://127.0.0.1:8000/reduce-quantity/${id_produto}`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${JSON.parse(token)["access_token"]}`
          },
        });
        
        const data = await res.json();
        const retorno = data;
        console.log(retorno)

        const updatedItems = items.map(item => {
          if (item.id === retorno.id) {
            return { ...item, quantidade: retorno.quantidade };
          }
          return item;
        });

        setItems(updatedItems);

      } catch (error) {
        console.error('Erro ao adicionar quantidade ao carrinho:', error);
      }
    }
  };

  const deleteItem = async (id_produto: string) => {
    const token = localStorage.getItem('token');
      if (token) {
        try {
          const res = await fetch(`http://127.0.0.1:8000/remove-item/${id_produto}/`, {
            method: 'DELETE',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${JSON.parse(token)["access_token"]}`
            },
          });
          const data = await res.json();

          const updatedItems = items.slice();
          const indexToRemove = updatedItems.findIndex(item => item.id === data.id);

          if (indexToRemove !== -1) {
            updatedItems.splice(indexToRemove, 1);
            setItems(updatedItems);
          }

        } catch (error) {
          console.error('Erro ao excluir item do carrinho:', error);
        };
    }
  };

  const confirmOrder = async () => {
    const token = localStorage.getItem('token');
      if (token) {
        try {
          const res = await fetch(`http://127.0.0.1:8000/update-status-pedido/`, {
            method: 'PATCH',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${JSON.parse(token)["access_token"]}`
            },
          });
          const data = res.json();
          console.log(data)
          setItems([]);
        } catch (error) {
          console.error('Erro ao confirmar pedido:', error);
        };
      };
  };

  let total:number = 0;

  if (items.length > 0) {
    total = items.reduce((acc, item) => acc + parseFloat(item.preco) * item.quantidade, 0);
  }

  return (
    <main className='flex justify-center h-screen bg-whitehistorico mt-28'>{/*configuração geral da pagina */}
      <div className='flex flex-col items-center w-full'>{/*centralização geral das tabelas,botões*/}
        <div className='mt-12 w-3/4 h-screen'>
          <div className='border-b border-tableBorder mb-4 w-1/6 ml-4'>{/*responsável pelo titulo*/}
            <h1 className='bg-gray text-xl font-semibold mx-auto'> MEU CARRINHO</h1>
          </div>{/*responsável pelo titulo*/}

          <div> {/*guardas as tabelas e os botões*/}
            <Table className="border-t border-tableBorder">
              <TableHeader>
                <TableRow>
                  <TableCell className="text-center text-xl p-1 border-l border-tableBorder">Produto</TableCell>
                  <TableCell className="text-center text-xl p-1">Preço</TableCell>
                  <TableCell className="text-center text-xl p-1 border-r border-tableBorder">Quantidade</TableCell>
                </TableRow>
              </TableHeader>

              <TableBody className="border-2 border-tableBorder">
                {items.length > 0 ? (
                  items.map((item) => (
                    <TableRow key={item.id}>
                      <TableCell className="text-center p-5 2/5">
                        <div className="flex items-center ml-6">
                          <Button
                            variant="ghost"
                            size="default"
                            className="mr-4"
                            onClick={() => deleteItem(item.id)}>
                            <Trash2 color="#ff0000"/>
                          </Button>
                          <div className=" h-24 w-24 text-lg">
                            <img src={DEFAULT_IMAGE_URL} alt={item.nome_produto} className="w-full h-full object-cover mb-4" />
                          </div>
                          <div className="ml-4">{item.nome_produto}</div>
                        </div>
                      </TableCell>

                      <TableCell className="text-center text-lg w-2/5">R$ {item.preco}</TableCell>

                      <TableCell className="text-center w-1/5">
                        <div className="flex justify-center items-center space-between">
                          <Button
                            variant="ghost"
                            size="default"
                            className="mr-2"
                            onClick={item.quantidade > 1 ? () => reduceQuantity(item.id) : () => deleteItem(item.id)}>
                            <Minus color="#000000" />
                          </Button>
                          <Input type="text" className="border border-tableBorder w-10 text-center" readOnly value={item.quantidade.toString()} />
                          <div className="flex justify-center items-center">
                          <Button
                            variant="ghost"
                            size="default"
                            className="ml-2"
                            onClick={() => incrementQuantity(item.id)}>
                            <Plus color="#000000" />
                          </Button>
                          </div>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))
                ) : (
                  <TableRow>
                    <TableCell colSpan={3} className="text-center">
                      <ShoppingBag color="#000000" />
                      <Label>Seu carrinho está vazio</Label>
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>

            <div className='mt-8'>{/*tabela de informações*/}
              <Table className="border border-tableBorder">
                <TableBody>
                  <TableRow>
                    <TableCell className="text-center py-4">Entrega</TableCell>
                    <TableCell className="text-center py-4 mt-2">
                      <div className='flex flex-col'>
                        <Label>FRETE GRÁTIS</Label>
                        <Label className='mt-2'>Pernambuco</Label>
                      </div>
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell className="text-center py-4">Total</TableCell>
                    <TableCell className="text-center text-lg  py-4">R$ {total.toFixed(2)}</TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </div>{/*tabela de informações*/}

            <div className='flex justify-end mt-5 gap-2'>{/*div dos botões*/}
              <Button
                  className='bg-trash'
                  type="submit"
                  variant="default"
                  size="default"
                  onClick={() => clearCart()}
                >
                  Limpar
                </Button>
                <Button
                  className='bg-green-success'
                  type="submit"
                  variant="default"
                  size="default"
                  onClick={() => confirmOrder()}
                >
                  Confirmar
                </Button>
            </div>{/*div dos botões*/}

          </div>
        </div>{/*guardas as tabelas e os botões*/}
      </div>{/*centralização geral das tabelas,botões*/}
{/*configuração geral da pagina */}</main>
  );
}

export default cartPage;