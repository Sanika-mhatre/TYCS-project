#!/usr/bin/env python3
"""
Test script for Academic Paper Reviewer
Tests the ML analysis functionality
"""

from app import analyze_paper_ml

def test_analysis():
    """Test the ML analysis function with sample text"""
    
    # Sample academic paper text
    sample_text = """
    Abstract
    This research paper presents a comprehensive study on machine learning approaches 
    in computer vision applications. The methodology involves deep learning techniques 
    and convolutional neural networks for image recognition tasks.
    
    Introduction
    Computer vision has emerged as a significant field in artificial intelligence.
    Recent studies have shown promising results in object detection and image 
    classification using advanced neural network architectures.
    
    Methodology
    Our approach utilizes state-of-the-art deep learning frameworks including 
    TensorFlow and PyTorch. The experimental setup involves training on large 
    datasets and implementing data augmentation techniques.
    
    Results
    The findings demonstrate improved accuracy rates of 95% on benchmark datasets.
    The proposed method outperforms existing approaches by 12% in precision metrics.
    
    Conclusion
    This study contributes to the advancement of computer vision research and 
    provides evidence for the effectiveness of deep learning in image analysis tasks.
    
    References
    [1] Smith, J. et al. (2023). Deep Learning in Computer Vision. Journal of AI Research.
    [2] Johnson, A. (2022). Neural Networks for Image Recognition. IEEE Transactions.
    """
    
    print("🔬 Testing ML Analysis Function...")
    print("=" * 50)
    
    # Perform analysis
    analysis = analyze_paper_ml(sample_text, "Test Paper")
    
    if analysis:
        print("✅ Analysis completed successfully!")
        print(f"📊 Overall Score: {analysis['overall_score']}/10")
        print(f"📝 Word Count: {analysis['word_count']}")
        print(f"📖 Readability: {analysis['readability_score']}/10")
        print(f"🎯 Keyword Density: {analysis['keyword_density']}%")
        print(f"📋 Structure Score: {analysis['structure_score']}/6")
        
        print("\n📋 Paper Structure:")
        for section, has_it in analysis['has_sections'].items():
            icon = "✅" if has_it else "❌"
            print(f"  {icon} {section.title()}")
        
        print("\n💡 Suggestions:")
        for suggestion in analysis['suggestions']:
            print(f"  • {suggestion}")
        
        print("\n🎉 Test completed successfully!")
        return True
    else:
        print("❌ Analysis failed!")
        return False

def test_demo_data():
    """Test demo data creation"""
    try:
        from demo import create_sample_data
        reviews, feedback = create_sample_data()
        
        print("\n🎯 Testing Demo Data...")
        print("=" * 50)
        print(f"✅ Created {len(reviews)} sample reviews")
        print(f"✅ Created {len(feedback)} sample feedback entries")
        
        # Display sample review
        sample_review = reviews[0]
        print(f"\n📄 Sample Review: {sample_review['title']}")
        print(f"   Score: {sample_review['overall_score']}/10")
        print(f"   Category: {sample_review['category']}")
        
        return True
    except Exception as e:
        print(f"❌ Demo data test failed: {e}")
        return False

if __name__ == "__main__":
    print("🎓 Academic Paper Reviewer - Test Suite")
    print("=" * 60)
    
    # Run tests
    test1_passed = test_analysis()
    test2_passed = test_demo_data()
    
    print("\n" + "=" * 60)
    print("📊 Test Results:")
    print(f"  ML Analysis Test: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"  Demo Data Test: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 All tests passed! The application is ready to use.")
        print("\n🚀 To run the application:")
        print("   streamlit run app.py")
    else:
        print("\n⚠️  Some tests failed. Please check the requirements and dependencies.")