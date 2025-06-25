import React from 'react';
import { motion } from 'framer-motion';
import { Star, Heart } from 'lucide-react';

const TestimonialsSection = ({ fadeInUp, staggerContainer }) => {
  const testimonials = [
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
  ];

  return (
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
          {testimonials.map((testimonial, index) => (
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
  );
};

export default TestimonialsSection;