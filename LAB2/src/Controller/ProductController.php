<?php

namespace App\Controller;

use App\Entity\Product;
use App\Repository\ProductRepository;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Routing\Annotation\Route;

#[Route('/api/products')]
class ProductController extends AbstractController
{
    public function __construct(
        private EntityManagerInterface $em,
        private ProductRepository $productRepository,
    ) {}

    #[Route('', methods: ['GET'])]
    public function index(): JsonResponse
    {
        $products = $this->productRepository->findAll();
        return $this->json(array_map(fn($p) => $p->toArray(), $products));
    }

    #[Route('/{id}', methods: ['GET'])]
    public function show(int $id): JsonResponse
    {
        $product = $this->productRepository->find($id);
        if (!$product) {
            return $this->json(['error' => 'Product not found'], 404);
        }
        return $this->json($product->toArray());
    }

    #[Route('', methods: ['POST'])]
    public function create(Request $request): JsonResponse
    {
        $data = json_decode($request->getContent(), true);

        if (!isset($data['name'], $data['price'])) {
            return $this->json(['error' => 'name and price are required'], 400);
        }

        $product = new Product();
        $product->setName($data['name']);
        $product->setPrice((float) $data['price']);
        $product->setDescription($data['description'] ?? null);

        $this->em->persist($product);
        $this->em->flush();

        return $this->json($product->toArray(), 201);
    }

    #[Route('/{id}', methods: ['PUT'])]
    public function update(int $id, Request $request): JsonResponse
    {
        $product = $this->productRepository->find($id);
        if (!$product) {
            return $this->json(['error' => 'Product not found'], 404);
        }

        $data = json_decode($request->getContent(), true);

        if (isset($data['name'])) {
            $product->setName($data['name']);
        }
        if (isset($data['price'])) {
            $product->setPrice((float) $data['price']);
        }
        if (array_key_exists('description', $data)) {
            $product->setDescription($data['description']);
        }

        $this->em->flush();

        return $this->json($product->toArray());
    }

    #[Route('/{id}', methods: ['DELETE'])]
    public function delete(int $id): JsonResponse
    {
        $product = $this->productRepository->find($id);
        if (!$product) {
            return $this->json(['error' => 'Product not found'], 404);
        }

        $this->em->remove($product);
        $this->em->flush();

        return $this->json(['message' => 'Product deleted']);
    }
}
