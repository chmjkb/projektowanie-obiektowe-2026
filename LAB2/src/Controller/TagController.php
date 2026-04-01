<?php

namespace App\Controller;

use App\Entity\Tag;
use App\Repository\TagRepository;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Routing\Annotation\Route;

#[Route('/api/tags')]
class TagController extends AbstractController
{
    public function __construct(
        private EntityManagerInterface $em,
        private TagRepository $tagRepository,
    ) {}

    #[Route('', methods: ['GET'])]
    public function index(): JsonResponse
    {
        $tags = $this->tagRepository->findAll();
        return $this->json(array_map(fn($t) => $t->toArray(), $tags));
    }

    #[Route('/{id}', methods: ['GET'])]
    public function show(int $id): JsonResponse
    {
        $tag = $this->tagRepository->find($id);
        if (!$tag) {
            return $this->json(['error' => 'Tag not found'], 404);
        }
        return $this->json($tag->toArray());
    }

    #[Route('', methods: ['POST'])]
    public function create(Request $request): JsonResponse
    {
        $data = json_decode($request->getContent(), true);

        if (!isset($data['name'])) {
            return $this->json(['error' => 'name is required'], 400);
        }

        $tag = new Tag();
        $tag->setName($data['name']);
        $tag->setColor($data['color'] ?? null);

        $this->em->persist($tag);
        $this->em->flush();

        return $this->json($tag->toArray(), 201);
    }

    #[Route('/{id}', methods: ['PUT'])]
    public function update(int $id, Request $request): JsonResponse
    {
        $tag = $this->tagRepository->find($id);
        if (!$tag) {
            return $this->json(['error' => 'Tag not found'], 404);
        }

        $data = json_decode($request->getContent(), true);

        if (isset($data['name'])) {
            $tag->setName($data['name']);
        }
        if (array_key_exists('color', $data)) {
            $tag->setColor($data['color']);
        }

        $this->em->flush();

        return $this->json($tag->toArray());
    }

    #[Route('/{id}', methods: ['DELETE'])]
    public function delete(int $id): JsonResponse
    {
        $tag = $this->tagRepository->find($id);
        if (!$tag) {
            return $this->json(['error' => 'Tag not found'], 404);
        }

        $this->em->remove($tag);
        $this->em->flush();

        return $this->json(['message' => 'Tag deleted']);
    }
}
