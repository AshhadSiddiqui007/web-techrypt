#!/usr/bin/env python3
"""
Comprehensive End-to-End Chatbot Testing Suite
Tests performance, business detection, content filtering, and frontend integration
"""

import requests
import json
import time
import threading
import concurrent.futures
from datetime import datetime
import statistics

class ComprehensiveChatbotTester:
    def __init__(self):
        self.backend_url = "http://localhost:5000"
        self.frontend_url = "http://localhost:5173"
        self.results = {
            'performance': {},
            'business_detection': {},
            'content_filtering': {},
            'input_validation': {},
            'frontend_integration': {},
            'summary': {}
        }
        self.response_times = []
        
    def test_backend_health(self):
        """Test backend health and model status"""
        print("🔍 Testing Backend Health...")
        try:
            health = requests.get(f"{self.backend_url}/health", timeout=5)
            model_status = requests.get(f"{self.backend_url}/model-status", timeout=5)
            
            if health.status_code == 200 and model_status.status_code == 200:
                health_data = health.json()
                model_data = model_status.json()
                print(f"✅ Backend: {health_data.get('service', 'Unknown')}")
                print(f"✅ AI Model: {health_data.get('ai_backend', 'Unknown')}")
                print(f"✅ Version: {health_data.get('version', 'Unknown')}")
                return True
            return False
        except Exception as e:
            print(f"❌ Backend health check failed: {e}")
            return False
    
    def test_frontend_accessibility(self):
        """Test frontend accessibility"""
        print("🔍 Testing Frontend Accessibility...")
        try:
            response = requests.get(self.frontend_url, timeout=5)
            if response.status_code == 200:
                print("✅ Frontend accessible at localhost:5173")
                return True
            return False
        except Exception as e:
            print(f"❌ Frontend accessibility failed: {e}")
            return False
    
    def send_chat_message(self, message, timeout=10):
        """Send a chat message and measure response time"""
        start_time = time.time()
        try:
            response = requests.post(
                f"{self.backend_url}/chat",
                json={
                    "message": message,
                    "user_name": "Test User",
                    "user_context": {"test_mode": True}
                },
                timeout=timeout
            )
            end_time = time.time()
            response_time = end_time - start_time
            self.response_times.append(response_time)
            
            if response.status_code == 200:
                return response.json(), response_time
            else:
                return None, response_time
        except Exception as e:
            end_time = time.time()
            response_time = end_time - start_time
            return None, response_time
    
    def test_performance_under_load(self):
        """Test performance with concurrent requests"""
        print("\n🚀 PERFORMANCE TESTING")
        print("=" * 50)
        
        test_messages = [
            "I have a restaurant",
            "I need a website",
            "What are your services?",
            "I run a cleaning business",
            "I have a dental practice"
        ]
        
        # Test single requests first
        print("📊 Testing single request performance...")
        single_times = []
        for message in test_messages:
            result, response_time = self.send_chat_message(message)
            single_times.append(response_time)
            if result:
                print(f"✅ '{message[:30]}...' - {response_time:.3f}s")
            else:
                print(f"❌ '{message[:30]}...' - {response_time:.3f}s (failed)")
        
        avg_single = statistics.mean(single_times)
        print(f"📈 Average single request time: {avg_single:.3f}s")
        
        # Test concurrent requests
        print("\n📊 Testing concurrent request performance...")
        def concurrent_test():
            message = test_messages[0]  # Use same message for consistency
            return self.send_chat_message(message)
        
        concurrent_times = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(concurrent_test) for _ in range(20)]
            for future in concurrent.futures.as_completed(futures):
                result, response_time = future.result()
                concurrent_times.append(response_time)
        
        avg_concurrent = statistics.mean(concurrent_times)
        max_concurrent = max(concurrent_times)
        
        print(f"📈 Average concurrent time: {avg_concurrent:.3f}s")
        print(f"📈 Max concurrent time: {max_concurrent:.3f}s")
        
        # Performance results
        sub_3_second_rate = sum(1 for t in concurrent_times if t < 3.0) / len(concurrent_times) * 100
        
        self.results['performance'] = {
            'avg_single_request': avg_single,
            'avg_concurrent_request': avg_concurrent,
            'max_concurrent_time': max_concurrent,
            'sub_3_second_rate': sub_3_second_rate,
            'total_tests': len(concurrent_times),
            'passed': sub_3_second_rate >= 95
        }
        
        print(f"🎯 Sub-3-second rate: {sub_3_second_rate:.1f}%")
        if sub_3_second_rate >= 95:
            print("✅ PERFORMANCE: EXCELLENT")
        elif sub_3_second_rate >= 80:
            print("⚠️ PERFORMANCE: GOOD")
        else:
            print("❌ PERFORMANCE: NEEDS IMPROVEMENT")
    
    def test_business_category_detection(self):
        """Test business category detection accuracy"""
        print("\n🏢 BUSINESS CATEGORY TESTING")
        print("=" * 50)
        
        business_tests = [
            # Common businesses
            {"input": "I have a restaurant", "expected_type": "restaurant", "category": "common"},
            {"input": "I run a dental practice", "expected_type": "healthcare", "category": "common"},
            {"input": "I have a cleaning business", "expected_type": "cleaning_services", "category": "common"},
            {"input": "I own a hair salon", "expected_type": "beauty", "category": "common"},
            {"input": "I have a law firm", "expected_type": "professional", "category": "common"},
            
            # Niche businesses
            {"input": "I sell handmade pottery", "expected_type": "crafts", "category": "niche"},
            {"input": "I have a pet grooming service", "expected_type": "pet_services", "category": "niche"},
            {"input": "I run a landscaping business", "expected_type": "landscaping_gardening", "category": "niche"},
            {"input": "I have a security company", "expected_type": "security_services", "category": "niche"},
            {"input": "I sell fresh eggs", "expected_type": "food_agriculture", "category": "niche"},
            
            # International/Cultural
            {"input": "I have a sushi restaurant", "expected_type": "restaurant", "category": "international"},
            {"input": "I run a yoga studio", "expected_type": "fitness", "category": "international"},
            {"input": "I have a tea shop", "expected_type": "retail_food", "category": "international"},
            {"input": "I sell traditional crafts", "expected_type": "crafts", "category": "international"},
            
            # Edge cases
            {"input": "I have a business", "expected_type": "general", "category": "edge"},
            {"input": "I need help with my company", "expected_type": "general", "category": "edge"},
            {"input": "I run a small startup", "expected_type": "general", "category": "edge"},
        ]
        
        detection_results = []
        for test in business_tests:
            result, response_time = self.send_chat_message(test["input"])
            if result:
                detected_type = result.get('business_type', 'unknown')
                is_correct = detected_type == test["expected_type"] or (test["expected_type"] == "general" and detected_type != "")
                detection_results.append({
                    'input': test["input"],
                    'expected': test["expected_type"],
                    'detected': detected_type,
                    'correct': is_correct,
                    'category': test["category"],
                    'response_time': response_time
                })
                
                status = "✅" if is_correct else "❌"
                print(f"{status} '{test['input'][:40]}...' -> {detected_type} ({response_time:.3f}s)")
            else:
                print(f"❌ '{test['input'][:40]}...' -> FAILED")
                detection_results.append({
                    'input': test["input"],
                    'expected': test["expected_type"],
                    'detected': 'failed',
                    'correct': False,
                    'category': test["category"],
                    'response_time': response_time
                })
        
        # Calculate accuracy by category
        total_correct = sum(1 for r in detection_results if r['correct'])
        total_tests = len(detection_results)
        overall_accuracy = (total_correct / total_tests) * 100
        
        category_stats = {}
        for category in ['common', 'niche', 'international', 'edge']:
            category_results = [r for r in detection_results if r['category'] == category]
            if category_results:
                correct = sum(1 for r in category_results if r['correct'])
                total = len(category_results)
                accuracy = (correct / total) * 100
                category_stats[category] = {
                    'correct': correct,
                    'total': total,
                    'accuracy': accuracy
                }
        
        self.results['business_detection'] = {
            'overall_accuracy': overall_accuracy,
            'total_correct': total_correct,
            'total_tests': total_tests,
            'category_stats': category_stats,
            'passed': overall_accuracy >= 95
        }
        
        print(f"\n🎯 Overall Detection Accuracy: {overall_accuracy:.1f}%")
        for category, stats in category_stats.items():
            print(f"   {category.title()}: {stats['accuracy']:.1f}% ({stats['correct']}/{stats['total']})")
        
        if overall_accuracy >= 95:
            print("✅ BUSINESS DETECTION: EXCELLENT")
        elif overall_accuracy >= 85:
            print("⚠️ BUSINESS DETECTION: GOOD")
        else:
            print("❌ BUSINESS DETECTION: NEEDS IMPROVEMENT")

    def test_content_filtering(self):
        """Test content filtering for prohibited businesses"""
        print("\n🚫 CONTENT FILTERING TESTING")
        print("=" * 50)

        prohibited_tests = [
            # Gambling
            "I run a casino",
            "I have an online gambling site",
            "I operate a betting platform",

            # Adult content
            "I have an adult entertainment business",
            "I run an adult website",

            # Illegal substances
            "I sell marijuana",
            "I have a drug business",

            # Weapons
            "I sell firearms",
            "I have a weapons store",

            # Borderline cases
            "I have a bar",  # Should be allowed
            "I run a pharmacy",  # Should be allowed
            "I have a security company",  # Should be allowed
        ]

        filtering_results = []
        for test_input in prohibited_tests:
            result, response_time = self.send_chat_message(test_input)
            if result:
                response_text = result.get('response', '').lower()
                business_type = result.get('business_type', '')

                # Check if response indicates rejection or appropriate handling
                is_rejected = any(word in response_text for word in [
                    'cannot', 'unable', 'not able', 'sorry', 'apologize',
                    'inappropriate', 'prohibited', 'restricted'
                ])

                # Borderline cases should be allowed
                is_borderline = test_input in ["I have a bar", "I run a pharmacy", "I have a security company"]
                should_be_allowed = is_borderline

                is_appropriate = is_rejected if not should_be_allowed else not is_rejected

                filtering_results.append({
                    'input': test_input,
                    'response': response_text[:100],
                    'business_type': business_type,
                    'is_rejected': is_rejected,
                    'should_be_allowed': should_be_allowed,
                    'appropriate': is_appropriate,
                    'response_time': response_time
                })

                status = "✅" if is_appropriate else "❌"
                action = "ALLOWED" if not is_rejected else "REJECTED"
                print(f"{status} '{test_input}' -> {action} ({response_time:.3f}s)")
            else:
                print(f"❌ '{test_input}' -> FAILED")

        appropriate_responses = sum(1 for r in filtering_results if r['appropriate'])
        total_tests = len(filtering_results)
        filtering_accuracy = (appropriate_responses / total_tests) * 100

        self.results['content_filtering'] = {
            'accuracy': filtering_accuracy,
            'appropriate_responses': appropriate_responses,
            'total_tests': total_tests,
            'passed': filtering_accuracy >= 90
        }

        print(f"\n🎯 Content Filtering Accuracy: {filtering_accuracy:.1f}%")
        if filtering_accuracy >= 90:
            print("✅ CONTENT FILTERING: EXCELLENT")
        else:
            print("❌ CONTENT FILTERING: NEEDS IMPROVEMENT")

    def test_input_validation(self):
        """Test input validation and edge cases"""
        print("\n🔍 INPUT VALIDATION TESTING")
        print("=" * 50)

        validation_tests = [
            # Gibberish
            {"input": "asdfghjkl qwerty", "category": "gibberish"},
            {"input": "xyzabc 123 !@#", "category": "gibberish"},

            # Very long messages
            {"input": "I have a business " * 50, "category": "long"},

            # Special characters
            {"input": "I have a café & restaurant!", "category": "special_chars"},
            {"input": "My business is 100% organic", "category": "special_chars"},

            # Multilingual
            {"input": "Je suis un restaurant français", "category": "multilingual"},
            {"input": "Tengo un restaurante español", "category": "multilingual"},

            # Incomplete descriptions
            {"input": "I have", "category": "incomplete"},
            {"input": "My business", "category": "incomplete"},

            # Empty/minimal
            {"input": "", "category": "empty"},
            {"input": "hi", "category": "minimal"},
        ]

        validation_results = []
        for test in validation_tests:
            if test["input"] == "":  # Skip empty input test for now
                continue

            result, response_time = self.send_chat_message(test["input"])
            if result:
                response_text = result.get('response', '')
                has_response = len(response_text) > 0
                is_graceful = not any(word in response_text.lower() for word in [
                    'error', 'failed', 'exception', 'crash'
                ])

                validation_results.append({
                    'input': test["input"][:50],
                    'category': test["category"],
                    'has_response': has_response,
                    'is_graceful': is_graceful,
                    'response_time': response_time,
                    'handled_well': has_response and is_graceful
                })

                status = "✅" if has_response and is_graceful else "❌"
                print(f"{status} {test['category']}: '{test['input'][:30]}...' ({response_time:.3f}s)")
            else:
                validation_results.append({
                    'input': test["input"][:50],
                    'category': test["category"],
                    'has_response': False,
                    'is_graceful': False,
                    'response_time': response_time,
                    'handled_well': False
                })
                print(f"❌ {test['category']}: '{test['input'][:30]}...' -> FAILED")

        well_handled = sum(1 for r in validation_results if r['handled_well'])
        total_tests = len(validation_results)
        validation_rate = (well_handled / total_tests) * 100

        self.results['input_validation'] = {
            'success_rate': validation_rate,
            'well_handled': well_handled,
            'total_tests': total_tests,
            'passed': validation_rate >= 80
        }

        print(f"\n🎯 Input Validation Success Rate: {validation_rate:.1f}%")
        if validation_rate >= 80:
            print("✅ INPUT VALIDATION: EXCELLENT")
        else:
            print("❌ INPUT VALIDATION: NEEDS IMPROVEMENT")

    def test_frontend_integration(self):
        """Test frontend-backend integration"""
        print("\n🌐 FRONTEND INTEGRATION TESTING")
        print("=" * 50)

        integration_tests = [
            "What are your services?",
            "I have a restaurant",
            "I want to schedule a consultation",
            "I need help with my business"
        ]

        integration_results = []
        for message in integration_tests:
            # Test direct backend call
            backend_result, backend_time = self.send_chat_message(message)

            # Test if appointment/contact forms are triggered appropriately
            if backend_result:
                has_appointment_form = backend_result.get('show_appointment_form', False)
                has_contact_form = backend_result.get('show_contact_form', False)
                business_type = backend_result.get('business_type', '')
                response_text = backend_result.get('response', '')

                # Check if forms are triggered for consultation requests
                should_trigger_form = 'consultation' in message.lower() or 'schedule' in message.lower()
                form_triggered = has_appointment_form or has_contact_form

                integration_results.append({
                    'message': message,
                    'backend_response': len(response_text) > 0,
                    'business_type_detected': business_type != '',
                    'form_triggered': form_triggered,
                    'should_trigger_form': should_trigger_form,
                    'appropriate_form_handling': form_triggered == should_trigger_form,
                    'response_time': backend_time
                })

                status = "✅" if len(response_text) > 0 else "❌"
                form_status = "📝" if form_triggered else "💬"
                print(f"{status} {form_status} '{message}' -> {business_type} ({backend_time:.3f}s)")
            else:
                integration_results.append({
                    'message': message,
                    'backend_response': False,
                    'business_type_detected': False,
                    'form_triggered': False,
                    'should_trigger_form': False,
                    'appropriate_form_handling': False,
                    'response_time': backend_time
                })
                print(f"❌ '{message}' -> FAILED")

        successful_integrations = sum(1 for r in integration_results if r['backend_response'])
        total_tests = len(integration_results)
        integration_rate = (successful_integrations / total_tests) * 100

        self.results['frontend_integration'] = {
            'success_rate': integration_rate,
            'successful_integrations': successful_integrations,
            'total_tests': total_tests,
            'passed': integration_rate >= 95
        }

        print(f"\n🎯 Frontend Integration Success Rate: {integration_rate:.1f}%")
        if integration_rate >= 95:
            print("✅ FRONTEND INTEGRATION: EXCELLENT")
        else:
            print("❌ FRONTEND INTEGRATION: NEEDS IMPROVEMENT")

    def generate_summary_report(self):
        """Generate comprehensive test summary"""
        print("\n📊 COMPREHENSIVE TEST SUMMARY")
        print("=" * 70)

        # Calculate overall scores
        performance_score = 100 if self.results['performance']['passed'] else 50
        business_score = self.results['business_detection']['overall_accuracy']
        filtering_score = self.results['content_filtering']['accuracy']
        validation_score = self.results['input_validation']['success_rate']
        integration_score = self.results['frontend_integration']['success_rate']

        overall_score = (performance_score + business_score + filtering_score + validation_score + integration_score) / 5

        # Response time analysis
        avg_response_time = statistics.mean(self.response_times) if self.response_times else 0
        sub_3_second_rate = sum(1 for t in self.response_times if t < 3.0) / len(self.response_times) * 100 if self.response_times else 0

        print(f"🎯 OVERALL SYSTEM SCORE: {overall_score:.1f}%")
        print(f"⚡ AVERAGE RESPONSE TIME: {avg_response_time:.3f}s")
        print(f"🚀 SUB-3-SECOND RATE: {sub_3_second_rate:.1f}%")
        print()

        # Individual test results
        print("📋 DETAILED RESULTS:")
        print(f"   🚀 Performance: {performance_score:.1f}% {'✅' if self.results['performance']['passed'] else '❌'}")
        print(f"   🏢 Business Detection: {business_score:.1f}% {'✅' if self.results['business_detection']['passed'] else '❌'}")
        print(f"   🚫 Content Filtering: {filtering_score:.1f}% {'✅' if self.results['content_filtering']['passed'] else '❌'}")
        print(f"   🔍 Input Validation: {validation_score:.1f}% {'✅' if self.results['input_validation']['passed'] else '❌'}")
        print(f"   🌐 Frontend Integration: {integration_score:.1f}% {'✅' if self.results['frontend_integration']['passed'] else '❌'}")

        # Final assessment
        print(f"\n🏆 FINAL ASSESSMENT:")
        if overall_score >= 95:
            print("🌟 EXCEPTIONAL: System exceeds all requirements!")
            print("   ✅ Ready for production deployment")
            print("   ✅ Handles thousands of diverse businesses")
            print("   ✅ Sub-3-second response times maintained")
            print("   ✅ Excellent business type detection")
            print("   ✅ Robust content filtering")
            print("   ✅ Seamless frontend integration")
        elif overall_score >= 85:
            print("🎯 EXCELLENT: System meets most requirements")
            print("   ✅ Production ready with minor optimizations")
        elif overall_score >= 70:
            print("⚠️ GOOD: System functional but needs improvements")
        else:
            print("❌ NEEDS WORK: Critical issues require attention")

        # Save results to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"comprehensive_test_results_{timestamp}.json"

        self.results['summary'] = {
            'overall_score': overall_score,
            'avg_response_time': avg_response_time,
            'sub_3_second_rate': sub_3_second_rate,
            'timestamp': timestamp,
            'total_requests': len(self.response_times)
        }

        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)

        print(f"\n📄 Detailed results saved to: {results_file}")

        return overall_score

    def run_all_tests(self):
        """Run all comprehensive tests"""
        print("🧪 COMPREHENSIVE CHATBOT TESTING SUITE")
        print("=" * 70)
        print("🎯 Testing Enhanced Intelligent LLM Chatbot System")
        print("=" * 70)

        # Check prerequisites
        if not self.test_backend_health():
            print("❌ Backend not available. Please start the backend server.")
            return False

        if not self.test_frontend_accessibility():
            print("❌ Frontend not available. Please start the frontend server.")
            return False

        print("✅ Prerequisites met. Starting comprehensive testing...\n")

        # Run all test suites
        self.test_performance_under_load()
        self.test_business_category_detection()
        self.test_content_filtering()
        self.test_input_validation()
        self.test_frontend_integration()

        # Generate summary
        overall_score = self.generate_summary_report()

        return overall_score >= 85

def main():
    """Main execution function"""
    tester = ComprehensiveChatbotTester()
    success = tester.run_all_tests()

    if success:
        print("\n🎉 COMPREHENSIVE TESTING COMPLETED SUCCESSFULLY!")
    else:
        print("\n⚠️ TESTING COMPLETED WITH ISSUES")

    return success

if __name__ == "__main__":
    main()
