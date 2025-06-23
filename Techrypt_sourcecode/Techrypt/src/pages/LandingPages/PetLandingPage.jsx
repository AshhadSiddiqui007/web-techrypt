import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
  MessageCircle, Calendar, Globe, CheckCircle, X, Star, 
  ChevronDown, ChevronUp, Bot, Zap, Users, 
  BarChart3, Shield, Heart, Linkedin, Instagram, Menu
} from 'lucide-react'; // Make sure to import from lucide-react or your icon library


const PetLandingPage = () => {
  const [activeAccordion, setActiveAccordion] = useState(null); // Removed TypeScript notation
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);


  const toggleAccordion = (index) => { // Removed TypeScript notation
    setActiveAccordion(activeAccordion === index ? null : index);
  };

  const openBookingModal = () => {
    setBookingModalOpen(true);
  };

  const closeBookingModal = () => {
    setBookingModalOpen(false);
  };

  const fadeInUp = {
    initial: { opacity: 0, y: 60 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.6, ease: "easeOut" }
  };

  const staggerContainer = {
    animate: {
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  return (
    <div className="min-h-screen bg-dark text-white font-inter overflow-x-hidden">
      
      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <motion.div 
            variants={staggerContainer}
            initial="initial"
            animate="animate"
            className="grid lg:grid-cols-2 gap-12 items-center"
          >
            <div className="space-y-8">
              <motion.div variants={fadeInUp} className="space-y-6">
                <h1 className="text-5xl lg:text-7xl font-bold leading-tight">
                  Automate Your{' '}
                  <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-secondary">
                    Pet Business
                  </span>{' '}
                  with AI
                </h1>
                <p className="text-xl lg:text-2xl text-gray-300 leading-relaxed">
                  Bookings. Upsells. Reminders. All on Autopilot.
                </p>
              </motion.div>

              <motion.div variants={fadeInUp} className="flex flex-col sm:flex-row gap-4">
                <motion.button
                  whileHover={{ scale: 1.05, boxShadow: "0 0 30px rgba(0, 255, 194, 0.4)" }}
                  whileTap={{ scale: 0.95 }}
                  onClick={openBookingModal}
                  className="bg-primary text-dark px-8 py-4 rounded-xl text-lg font-semibold hover:bg-primary/90 transition-all duration-300 animate-glow"
                >
                  Book Free Demo
                </motion.button>
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="border-2 border-secondary text-secondary px-8 py-4 rounded-xl text-lg font-semibold hover:bg-secondary hover:text-dark transition-all duration-300"
                >
                  Watch Demo
                </motion.button>
              </motion.div>

              <motion.div variants={fadeInUp} className="flex items-center space-x-8 pt-4">
                <div className="flex items-center space-x-2">
                  <CheckCircle className="w-5 h-5 text-primary" />
                  <span className="text-gray-300">No Setup Required</span>
                </div>
                <div className="flex items-center space-x-2">
                  <CheckCircle className="w-5 h-5 text-primary" />
                  <span className="text-gray-300">24/7 Support</span>
                </div>
              </motion.div>
            </div>

            <motion.div 
              variants={fadeInUp}
              className="relative"
            >
              <div className="relative bg-gradient-to-br from-dark-lighter to-dark-light rounded-3xl p-8 border border-dark-light shadow-2xl animate-float">
                <div className="space-y-4">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 bg-primary rounded-full flex items-center justify-center">
                      <Bot className="w-6 h-6 text-dark" />
                    </div>
                    <div>
                      <h3 className="font-semibold">AI Assistant</h3>
                      <p className="text-sm text-gray-400">Online now</p>
                    </div>
                  </div>
                  
                  <div className="space-y-3">
                    <div className="bg-gray-700 rounded-2xl p-4 ml-8">
                      <p className="text-sm">Hi! I'd like to book a grooming appointment for my Golden Retriever.</p>
                    </div>
                    <div className="bg-primary/20 rounded-2xl p-4 mr-8">
                      <p className="text-sm">Perfect! I can help you with that. What day works best for you?</p>
                    </div>
                    <div className="bg-gray-700 rounded-2xl p-4 ml-8">
                      <p className="text-sm">How about this Friday afternoon?</p>
                    </div>
                    <div className="bg-primary/20 rounded-2xl p-4 mr-8">
                      <p className="text-sm">Friday at 2 PM is available! I've also added nail trimming - it's 20% off for new customers.</p>
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-4 sm:px-6 lg:px-8 bg-dark-lighter/50">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl lg:text-5xl font-bold mb-6">
              Why Pet Businesses{' '}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-secondary">
                Love Us
              </span>
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Transform your pet grooming business with AI that never sleeps, never forgets, and always upsells.
            </p>
          </motion.div>

          <motion.div
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            className="grid md:grid-cols-3 gap-8"
          >
            {[
              {
                icon: MessageCircle,
                title: "24/7 AI Chatbot",
                description: "Never miss a customer inquiry. Our AI responds instantly, books appointments, and answers questions around the clock."
              },
              {
                icon: Calendar,
                title: "Automated Booking System",
                description: "Smart scheduling that prevents double-bookings, sends reminders, and optimizes your calendar for maximum revenue."
              },
              {
                icon: Globe,
                title: "Multilingual Client Support",
                description: "Serve customers in their preferred language. Our AI speaks 50+ languages fluently and culturally adapts responses."
              }
            ].map((feature, index) => (
              <motion.div
                key={index}
                variants={fadeInUp}
                whileHover={{ y: -10, transition: { duration: 0.3 } }}
                className="bg-gradient-to-br from-dark-lighter to-dark-light rounded-2xl p-8 border border-dark-light hover:border-primary/50 transition-all duration-300 group"
              >
                <div className="w-16 h-16 bg-gradient-to-br from-primary to-secondary rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                  <feature.icon className="w-8 h-8 text-dark" />
                </div>
                <h3 className="text-2xl font-bold mb-4 group-hover:text-primary transition-colors">
                  {feature.title}
                </h3>
                <p className="text-gray-300 leading-relaxed">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Benefits Section */}
      <section id="benefits" className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="grid lg:grid-cols-2 gap-16 items-center"
          >
            <div className="space-y-8">
              <div>
                <h2 className="text-4xl lg:text-5xl font-bold mb-6">
                  More Bookings,{' '}
                  <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-secondary">
                    Less Work
                  </span>
                </h2>
                <p className="text-xl text-gray-300 leading-relaxed">
                  Our AI doesn't just answer questions—it actively grows your business while you focus on what you do best.
                </p>
              </div>

              <div className="space-y-6">
                {[
                  {
                    icon: Shield,
                    title: "No Missed Calls",
                    description: "Every inquiry gets an instant, professional response"
                  },
                  {
                    icon: BarChart3,
                    title: "More Bookings, Less Work",
                    description: "AI handles 80% of booking conversations automatically"
                  },
                  {
                    icon: Users,
                    title: "Works Everywhere",
                    description: "Website, WhatsApp, Instagram - one AI, all platforms"
                  }
                ].map((benefit, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -30 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: index * 0.1 }}
                    className="flex items-start space-x-4"
                  >
                    <div className="w-12 h-12 bg-gradient-to-br from-primary to-secondary rounded-xl flex items-center justify-center flex-shrink-0">
                      <benefit.icon className="w-6 h-6 text-dark" />
                    </div>
                    <div>
                      <h3 className="text-xl font-semibold mb-2">{benefit.title}</h3>
                      <p className="text-gray-300">{benefit.description}</p>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>

            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              className="relative"
            >
              <div className="bg-gradient-to-br from-dark-lighter to-dark-light rounded-3xl p-8 border border-dark-light shadow-2xl">
                <div className="space-y-6">
                  <div className="flex items-center justify-between">
                    <h3 className="text-2xl font-bold">Dashboard Analytics</h3>
                    <div className="flex space-x-2">
                      <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                      <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                      <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-dark rounded-xl p-4">
                      <div className="text-3xl font-bold text-primary">+127%</div>
                      <div className="text-sm text-gray-400">Bookings This Month</div>
                    </div>
                    <div className="bg-dark rounded-xl p-4">
                      <div className="text-3xl font-bold text-secondary">$15,420</div>
                      <div className="text-sm text-gray-400">Revenue Generated</div>
                    </div>
                    <div className="bg-dark rounded-xl p-4">
                      <div className="text-3xl font-bold text-primary">24/7</div>
                      <div className="text-sm text-gray-400">AI Availability</div>
                    </div>
                    <div className="bg-dark rounded-xl p-4">
                      <div className="text-3xl font-bold text-secondary">98%</div>
                      <div className="text-sm text-gray-400">Customer Satisfaction</div>
                    </div>
                  </div>

                  <div className="bg-dark rounded-xl p-4">
                    <div className="flex items-center justify-between mb-3">
                      <span className="text-sm text-gray-400">AI Performance</span>
                      <span className="text-sm text-primary">Excellent</span>
                    </div>
                    <div className="w-full bg-dark-light rounded-full h-2">
                      <div className="bg-gradient-to-r from-primary to-secondary h-2 rounded-full w-4/5"></div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="absolute -bottom-4 -right-4 w-24 h-24 bg-gradient-to-br from-primary to-secondary rounded-2xl opacity-20 animate-pulse"></div>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* Comparison Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-dark-lighter/50">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl lg:text-5xl font-bold mb-6">
              Techrypt AI vs{' '}
              <span className="text-gray-500">Traditional Software</span>
            </h2>
            <p className="text-xl text-gray-300">
              See why smart pet business owners are making the switch
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="bg-gradient-to-br from-dark-lighter to-dark-light rounded-3xl overflow-hidden border border-dark-light"
          >
            <div className="grid grid-cols-3 gap-0">
              <div className="p-6 border-r border-dark-light">
                <h3 className="text-xl font-bold text-center">Features</h3>
              </div>
              <div className="p-6 border-r border-dark-light bg-primary/10">
                <h3 className="text-xl font-bold text-center text-primary">Techrypt AI</h3>
              </div>
              <div className="p-6">
                <h3 className="text-xl font-bold text-center text-gray-400">Traditional</h3>
              </div>
            </div>

            {[
              ["24/7 AI Chatbot", true, false],
              ["Automated Upsells", true, false],
              ["50+ Languages", true, false],
              ["Real-Time Booking", true, true],
              ["WhatsApp Integration", true, false],
              ["Instagram DMs", true, false],
              ["Smart Reminders", true, true],
              ["Revenue Analytics", true, false]
            ].map(([feature, techrypt, traditional], index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="grid grid-cols-3 gap-0 border-t border-dark-light hover:bg-dark-light/30 transition-colors"
              >
                <div className="p-4 border-r border-dark-light">
                  <span className="font-medium">{feature}</span>
                </div>
                <div className="p-4 border-r border-dark-light bg-primary/5 text-center">
                  {techrypt ? (
                    <CheckCircle className="w-6 h-6 text-primary mx-auto" />
                  ) : (
                    <X className="w-6 h-6 text-gray-500 mx-auto" />
                  )}
                </div>
                <div className="p-4 text-center">
                  {traditional ? (
                    <CheckCircle className="w-6 h-6 text-gray-400 mx-auto" />
                  ) : (
                    <X className="w-6 h-6 text-gray-500 mx-auto" />
                  )}
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section id="testimonials" className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl lg:text-5xl font-bold mb-6">
              Loved by{' '}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-secondary">
                Pet Business Owners
              </span>
            </h2>
            <p className="text-xl text-gray-300">
              Real results from real pet grooming businesses
            </p>
          </motion.div>

          <motion.div
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            className="grid md:grid-cols-3 gap-8"
          >
            {[
              {
                name: "Sarah Johnson",
                business: "Pawsome Grooming Studio",
                rating: 5,
                quote: "Our bookings increased by 140% in just 2 months! The AI handles everything while I focus on grooming. Best investment I've made."
              },
              {
                name: "Mike Rodriguez",
                business: "Happy Tails Spa",
                rating: 5,
                quote: "I was skeptical about AI, but this is incredible. It books appointments, suggests add-ons, and even handles difficult customers better than I do!"
              },
              {
                name: "Emily Chen",
                business: "Urban Pet Care",
                rating: 5,
                quote: "The multilingual support opened up a whole new customer base. Our Spanish-speaking clients love that they can book in their native language."
              }
            ].map((testimonial, index) => (
              <motion.div
                key={index}
                variants={fadeInUp}
                whileHover={{ y: -10 }}
                className="bg-gradient-to-br from-dark-lighter to-dark-light rounded-2xl p-8 border border-dark-light hover:border-primary/30 transition-all duration-300"
              >
                <div className="flex items-center mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="w-5 h-5 text-yellow-400 fill-current" />
                  ))}
                </div>
                
                <p className="text-gray-300 mb-6 italic leading-relaxed">
                  "{testimonial.quote}"
                </p>
                
                <div className="flex items-center space-x-3">
                  <div className="w-12 h-12 bg-gradient-to-br from-primary to-secondary rounded-full flex items-center justify-center">
                    <Heart className="w-6 h-6 text-dark" />
                  </div>
                  <div>
                    <div className="font-semibold">{testimonial.name}</div>
                    <div className="text-sm text-gray-400">{testimonial.business}</div>
                  </div>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* FAQ Section */}
      <section id="faq" className="py-20 px-4 sm:px-6 lg:px-8 bg-dark-lighter/50">
        <div className="max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl lg:text-5xl font-bold mb-6">
              Frequently Asked{' '}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-secondary">
                Questions
              </span>
            </h2>
            <p className="text-xl text-gray-300">
              Everything you need to know about Techrypt AI
            </p>
          </motion.div>

          <motion.div
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            className="space-y-4"
          >
            {[
              {
                question: "How quickly can I set up Techrypt AI?",
                answer: "Setup takes less than 15 minutes. We provide a simple embed code for your website and connect your existing booking system. No technical expertise required!"
              },
              {
                question: "Does it integrate with my current booking software?",
                answer: "Yes! Techrypt AI integrates with all major pet grooming software including PetExec, Groomer.io, and others through our API connections."
              },
              {
                question: "What if the AI can't answer a customer's question?",
                answer: "Our AI is trained specifically for pet grooming businesses, but if it encounters something unusual, it seamlessly transfers the conversation to you with full context."
              },
              {
                question: "How much does it cost?",
                answer: "We offer flexible pricing starting at $97/month with no setup fees. Most businesses see ROI within the first month through increased bookings."
              },
              {
                question: "Can I customize the AI's responses?",
                answer: "Absolutely! You can customize pricing, services, policies, and even the AI's personality to match your brand voice perfectly."
              }
            ].map((faq, index) => (
              <motion.div
                key={index}
                variants={fadeInUp}
                className="bg-gradient-to-br from-dark-lighter to-dark-light rounded-2xl border border-dark-light overflow-hidden"
              >
                <button
                  className="w-full p-6 text-left flex items-center justify-between hover:bg-dark-light/30 transition-colors"
                  onClick={() => toggleAccordion(index)}
                >
                  <span className="text-lg font-semibold">{faq.question}</span>
                  {activeAccordion === index ? (
                    <ChevronUp className="w-6 h-6 text-primary" />
                  ) : (
                    <ChevronDown className="w-6 h-6 text-gray-400" />
                  )}
                </button>
                
                <motion.div
                  initial={false}
                  animate={{
                    height: activeAccordion === index ? "auto" : 0,
                    opacity: activeAccordion === index ? 1 : 0
                  }}
                  transition={{ duration: 0.3, ease: "easeInOut" }}
                  className="overflow-hidden"
                >
                  <div className="p-6 pt-0 text-gray-300 leading-relaxed">
                    {faq.answer}
                  </div>
                </motion.div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Final CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="space-y-8"
          >
            <h2 className="text-4xl lg:text-6xl font-bold">
              Start Automating{' '}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-secondary">
                Today
              </span>
            </h2>
            
            <p className="text-xl lg:text-2xl text-gray-300 max-w-2xl mx-auto">
              Join hundreds of pet businesses already using AI to grow their revenue while reducing workload
            </p>

            <motion.div className="flex flex-col sm:flex-row gap-4 justify-center">
              <motion.button
                whileHover={{ scale: 1.05, boxShadow: "0 0 40px rgba(0, 255, 194, 0.5)" }}
                whileTap={{ scale: 0.95 }}
                onClick={openBookingModal}
                className="bg-primary text-dark px-10 py-5 rounded-xl text-xl font-bold hover:bg-primary/90 transition-all duration-300 animate-glow"
              >
                Get Started for Free
              </motion.button>
              
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={openBookingModal}
                className="border-2 border-secondary text-secondary px-10 py-5 rounded-xl text-xl font-bold hover:bg-secondary hover:text-dark transition-all duration-300"
              >
                Schedule Demo
              </motion.button>
            </motion.div>

            <p className="text-gray-400">
              No credit card required • 14-day free trial • Cancel anytime
            </p>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-dark-lighter border-t border-dark-light py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-4 gap-8">
            <div className="space-y-4">
              <div className="flex items-center space-x-2">
                <Bot className="w-8 h-8 text-primary" />
                <span className="text-xl font-bold">Techrypt AI</span>
              </div>
              <p className="text-gray-400">
                AI-powered software for pet grooming businesses. Automate bookings, increase revenue, delight customers.
              </p>
              <div className="flex space-x-4">
                <motion.a
                  whileHover={{ scale: 1.1 }}
                  href="#"
                  className="w-10 h-10 bg-dark-light rounded-lg flex items-center justify-center hover:bg-primary hover:text-dark transition-colors"
                >
                  <Linkedin className="w-5 h-5" />
                </motion.a>
                <motion.a
                  whileHover={{ scale: 1.1 }}
                  href="#"
                  className="w-10 h-10 bg-dark-light rounded-lg flex items-center justify-center hover:bg-primary hover:text-dark transition-colors"
                >
                  <Instagram className="w-5 h-5" />
                </motion.a>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-4">Product</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-primary transition-colors">Features</a></li>
                <li><a href="#" className="hover:text-primary transition-colors">Pricing</a></li>
                <li><a href="#" className="hover:text-primary transition-colors">Integrations</a></li>
                <li><a href="#" className="hover:text-primary transition-colors">API</a></li>
              </ul>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-4">Company</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-primary transition-colors">About</a></li>
                <li><a href="#" className="hover:text-primary transition-colors">Blog</a></li>
                <li><a href="#" className="hover:text-primary transition-colors">Careers</a></li>
                <li><a href="#" className="hover:text-primary transition-colors">Contact</a></li>
              </ul>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-4">Support</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-primary transition-colors">Help Center</a></li>
                <li><a href="#" className="hover:text-primary transition-colors" onClick={openBookingModal}>Book Demo</a></li>
                <li><a href="#" className="hover:text-primary transition-colors">Status</a></li>
                <li><a href="#" className="hover:text-primary transition-colors">Privacy</a></li>
              </ul>
            </div>
          </div>

          <div className="border-t border-dark-light mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2024 Techrypt AI. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default PetLandingPage;