"""
Test script for RAG Resume Scorer
Run this to verify the application is working correctly
"""

import asyncio
from services_parser import parse_file


async def test_basic_parsing():
    """Test file parsing functionality"""
    print("Testing file parsing...")
    
    # Test with sample text
    sample_text = b"John Doe\nElectronic Engineer\nSkills: Python, FastAPI, ML"
    result = await parse_file(sample_text, "sample.txt")
    
    print(f"✓ Text parsing: {len(result)} characters")
    return True


async def test_embedding():
    """Test embedding generation"""
    print("\nTesting OpenAI embeddings...")
    try:
        from services_embeddings import get_embeddings
        
        texts = ["Hello world", "Python programming"]
        embeddings = get_embeddings(texts)
        
        print(f"✓ Generated {len(embeddings)} embeddings")
        print(f"✓ Embedding dimension: {len(embeddings[0])}")
        return True
    except Exception as e:
        print(f"✗ Embedding test failed: {e}")
        return False


async def test_rag():
    """Test RAG retriever"""
    print("\nTesting RAG retriever...")
    try:
        from services_rag import RAGRetriever
        
        sample_text = """
        I am an experienced Python developer with 5 years of experience.
        I have worked with FastAPI, Flask, and Django frameworks.
        My expertise includes machine learning, data analysis, and cloud deployment.
        I am proficient in AWS, Docker, and Kubernetes.
        """
        
        retriever = RAGRetriever(top_k=3)
        retriever.index_document(sample_text)
        
        query = "Python development experience"
        results = retriever.retrieve(query)
        
        print(f"✓ Retrieved {len(results)} relevant sections")
        return True
    except Exception as e:
        print(f"✗ RAG test failed: {e}")
        return False


async def test_api():
    """Test API health check"""
    print("\nTesting API...")
    try:
        from main import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        response = client.get("/api/health")
        
        if response.status_code == 200:
            print(f"✓ API Health check: {response.json()}")
            return True
        else:
            print(f"✗ API returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ API test failed: {e}")
        return False


async def main():
    """Run all tests"""
    print("\n" + "="*50)
    print("RAG Resume Scorer - Test Suite")
    print("="*50)
    
    tests = [
        ("Basic Parsing", test_basic_parsing),
        ("Embeddings", test_embedding),
        ("RAG Retriever", test_rag),
        ("API", test_api),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} failed: {e}")
            results.append((test_name, False))
    
    print("\n" + "="*50)
    print("Test Results:")
    print("="*50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed! Application is ready to use.")
    else:
        print(f"\n✗ {total - passed} test(s) failed. Check configuration.")


if __name__ == "__main__":
    asyncio.run(main())
