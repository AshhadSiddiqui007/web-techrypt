import React from "react";
import Blog_List_View from "../../components/BlogPage/Blog_List_View";


const BlogPage = () => {
  return (
    <div style={{ backgroundColor: "#0f0f0f" }} className="min-h-screen">
      <div className="container-responsive spacing-responsive-lg text-center">
        <h1 className="text-responsive-4xl md:text-6xl lg:text-7xl font-black text-white mb-8 md:mb-16 uppercase tracking-wider relative animate-fade-in">
          Blogs
          <span className="absolute -bottom-4 left-1/2 transform -translate-x-1/2 w-32 md:w-48 lg:w-60 h-1.5 bg-primary block animate-underline-grow"></span>
        </h1>
        
        <Blog_List_View />
      </div>
    </div>
  );
};

export default BlogPage;