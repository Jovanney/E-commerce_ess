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
  const DEFAULT_IMAGE_URL = "data:image/jpeg;base64,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";

  useEffect(() => {
    const fetchData = async () => {
      const token = localStorage.getItem('token');
      if (token) {
  
      try {
        const res = await fetch(`http://127.0.0.1:8000/pedidos/`, {
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
                            className="ml-2">
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