"use client";
import React, { useState, useEffect } from 'react';
import NavBar from '@/components/NavBar';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { toast, useToast } from "@/components/ui/use-toast"

interface ProductData {
  id_produto: number;
  cnpj_loja: string;
  categoria_prod: string;
  nome_produto: string;
  marca_produto: string;
  preco: string;
  especificacoes: string;
}

const ProductsByCnpjWithDelete = () => {
  const [cnpj, setCnpj] = useState('');
  const [products, setProducts] = useState<ProductData[]>([]);
  const [message, setMessage] = useState<string>('');
  const [selectedProduct, setSelectedProduct] = useState<ProductData | null>(null);
  const [newData, setNewData] = useState<Partial<ProductData>>({
    categoria_prod: '',
    nome_produto: '',
    marca_produto: '',
    preco: '',
    especificacoes: '',
  });

  const [productInEditMode, setProductInEditMode] = useState<number | null>(null);

  const handleSubmit = async () => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const res = await fetch(`http://127.0.0.1:8000/All_Produtos_cnpj`, {
          headers: {
            'Authorization': `Bearer ${JSON.parse(token)["access_token"]}`
          }
        });

        if (res.status === 200) {
          const productsData = await res.json();
          setProducts(productsData);
        } else if (res.status === 404) {
          toast({
            title: "Nenhum produto encontrado para o CNPJ.",
            description: "E-PASS",
          });
          //setMessage('Nenhum produto encontrado para o CNPJ.');
          setProducts([]);
        }
      } catch (error) {
        toast({
          title: "Erro em mostrar os produtos para este CNPJ",
          description: "E-PASS",
          style: {
            backgroundColor: "#FF0000", 
            color: "white" 
          }
        });
      }
    }
  };

  const handleCnpjChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setCnpj(event.target.value);
    setProducts([]);
    setMessage('');
    setSelectedProduct(null);
    setProductInEditMode(null);
  };

  const handleProductSelect = (product: ProductData) => {
    setSelectedProduct(product);
    setProductInEditMode(null);
  };

  const handleUpdateClick = (productId: number) => {
    setProductInEditMode(productId);
  };

  const handleNewDataChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setNewData({
      ...newData,
      [name]: value,
    });
  };

  const handleUpdateProduct = async (productId: number) => {
    try {
      const queryParams = new URLSearchParams();

      for (const [key, value] of Object.entries(newData)) {
        if (value !== "") {
          const valueAsString = typeof value === 'number' ? value.toString() : value;
          queryParams.append(key, valueAsString);
        }
      }

      const response = await fetch(
        `http://127.0.0.1:8000/update_produto/${productId}?${queryParams.toString()}`,
        {
          method: 'PUT',
        }
      );

      if (response.ok) {
        /* alert('Produto atualizado com sucesso'); */
        toast({
          title: "Produto atualizado com sucesso",
          description: "E-PASS",
          style: {
            backgroundColor: "#4CAF50", 
            color: "white" 
          }
        });
        setNewData({
          categoria_prod: '',
          nome_produto: '',
          marca_produto: '',
          preco: '',
          especificacoes: '',
        });
        setProductInEditMode(null);
        handleSubmit();
      } else {
        /* alert('Erro ao atualizar o produto'); */
        toast({
          title: "Erro ao atualizar o produto",
          description: "E-PASS",
          style: {
            backgroundColor: "#FF0000", 
            color: "white" 
          }
        });
      }
    } catch (error) {
      toast({
        title: "Erro ao atualizar o produto",
        description: "E-PASS",
        style: {
          backgroundColor: "#FF0000", 
          color: "white" 
        }
      });
      //console.error('Erro ao atualizar o produto:', error);
      /* alert('Erro ao atualizar o produto'); */
    }
  };

  const handleDelete = async (productId: number) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/del_produtos/${productId}`, {
        method: 'DELETE'
      });

      if (response.ok) {
        setProducts(products.filter(product => product.id_produto !== productId));
        //setMessage('Produto excluído com sucesso.');
        toast({
          title: "Produto deletado com sucesso",
          description: "E-PASS",
          style: {
            backgroundColor: "#4CAF50", 
            color: "white" 
          }
        });
        handleSubmit();
      } else {
        /*setMessage('Erro ao excluir o produto.'); */
        toast({
          title: "Erro ao excluir o produto.",
          description: "E-PASS",
          style: {
            backgroundColor: "#FF0000", 
            color: "white" 
          }
        });
      }
    } catch (error) {
      //console.error('Erro ao excluir o produto:', error);
      toast({
        title: "Erro ao excluir o produto.",
        description: "E-PASS",
        style: {
            backgroundColor: "#FF0000", 
            color: "white" 
          }
      });
    }
  };

  useEffect(() => {
    handleSubmit();
    setSelectedProduct(null);
    setProductInEditMode(null);
  }, []);

  return (
    <div className="w-full min-h-screen bg-whitehistorico">
      <NavBar />
  
      <div className="container mx-auto mt-10 pt-60">
        {products.length > 0 && (
          <div>
            <h2 className="text-2xl mb-4"><b>Seus produtos:</b></h2>
            {products.map(product => (
              <div key={product.id_produto} className="bg-white rounded-lg shadow-md p-6 mb-6 flex justify-between border border-black">
                <div>
                  <div className="mb-2">Categoria: {product.categoria_prod}</div>
                  <div className="mb-2">Nome: {product.nome_produto}</div>
                  <div className="mb-2">Marca: {product.marca_produto}</div>
                  <div className="mb-2">Preço: {product.preco}</div>
                  <div className="mb-2">Especificações: {product.especificacoes}</div>
                </div>
                
                {product.id_produto === productInEditMode ? (
                  <div className="flex flex-col mt-4">
                    <Label className="mb-2">Nova Categoria:</Label>
                    <Input
                      type="text"
                      name="categoria_prod"
                      value={newData.categoria_prod}
                      onChange={handleNewDataChange}
                      className="px-2 py-1 border rounded-md"
                    />
                    <Label className="mb-2">Novo Nome:</Label>
                    <Input
                      type="text"
                      name="nome_produto"
                      value={newData.nome_produto}
                      onChange={handleNewDataChange}
                      className="px-2 py-1 border rounded-md"
                    />
                    <Label className="mb-2">Nova Marca:</Label>
                    <Input
                      type="text"
                      name="marca_produto"
                      value={newData.marca_produto}
                      onChange={handleNewDataChange}
                      className="px-2 py-1 border rounded-md"
                    />
                    <Label className="mb-2">Novo Preço:</Label>
                    <Input
                      type="text"
                      name="preco"
                      value={newData.preco}
                      onChange={handleNewDataChange}
                      className="px-2 py-1 border rounded-md"
                    />
                    <Label className="mb-2">Novas Especificações:</Label>
                    <Input
                      type="text"
                      name="especificacoes"
                      value={newData.especificacoes}
                      onChange={handleNewDataChange}
                      className="px-2 py-1 border rounded-md"
                    />
                    <Button
                      className='bg-green-success text-white'
                      variant="default"
                      size="default"
                      onClick={() => {
                        handleUpdateProduct(product.id_produto);
                      }}
                    >
                      Confirmar Atualização
                    </Button>
                  </div>
                ) : (
                  <div className="flex space-x-2"> 
                    <Button
                      className='bg-green-success text-white'
                      variant="default"
                      size="default"
                      onClick={() => handleUpdateClick(product.id_produto)}
                    >
                      Alterar
                    </Button>
                    <Button
                      className='bg-red-cancel text-white'
                      variant="destructive"
                      size="default"
                      onClick={() => handleDelete(product.id_produto)}
                    >
                      Excluir
                    </Button>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ProductsByCnpjWithDelete;