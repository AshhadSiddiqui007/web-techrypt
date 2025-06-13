import React, { useState } from 'react';
import FilterRow from '../FilterRow/FilterRow';
import { data } from '../../assets/Data/Data';
import './Filter.css';

function Filter() {
  const [service, setService] = useState('');
  const [geo, setGeo] = useState('');
  const [vertical, setVertical] = useState('');
  const [visibleCount, setVisibleCount] = useState(6); // State to manage number of visible items

  // Function to filter data based on selected filters
  const filteredData = data.filter(item => {
    return (
      (service === '' || item.Services === service) &&
      (geo === '' || item.GEO === geo) &&
      (vertical === '' || item.Vertical === vertical)
    );
  });

  // Function to show more items
  const showMoreItems = () => {
    setVisibleCount(prevCount => prevCount + 6); // Show 6 more items on each click
  };

  return (
    <section className='filter-section'>
      <div className="filter-section-heading">
        {/*<h1 className='filter-h1 glowing-green'>Other Works</h1>*/}
      </div>
      <div className="filter-section-filter-container">
        <div className='filter-select'>
          <select className='' value={service} onChange={(e) => setService(e.target.value)}>
            <option value="">All Services</option>
            <option value="Influencer Marketing">Influencer Marketing</option>
            <option value="Performance Marketing">Performance Marketing</option>
            <option value="AI Chatbot Integration">AI Chatbot Integration</option>
            <option value="Website Development">Website Development</option>
            <option value="Ecommerce Store">Ecommerce Store</option>
          </select>

          <select value={geo} onChange={(e) => setGeo(e.target.value)}>
            <option value="">All Regions</option>
            <option value="North America">North America</option>
            <option value="Europe">Europe</option>
            <option value="Asia">Asia</option>
            <option value="Latin America">Latin America</option>
            <option value="WorldWide">WorldWide</option>
          </select>

          <select value={vertical} onChange={(e) => setVertical(e.target.value)}>
            <option value="">All Industries</option>
            <option value="Delivery">Delivery</option>
            <option value="E-commerce">E-commerce</option>
            <option value="Entertainment">Entertainment</option>
            <option value="Finance">Finance</option>
            <option value="Food & Drinks">Food & Drinks</option>
            <option value="Games">Games</option>
            <option value="Health">Health</option>
            <option value="Retail">Retail</option>
            <option value="Social">Social</option>
            <option value="Travel">Travel</option>
            <option value="Utilities">Utilities</option>
          </select>
        </div>

        <div className="filter-rows">
          {filteredData.slice(0, visibleCount).map((item, index) => (
            <div className="filter-row" key={index}>
              <FilterRow data={item} />
            </div>
          ))}
        </div>

        {/* Show the "Show More" button only if there are more items to display */}
        {visibleCount < filteredData.length && (
          <div className="show-more-container">
            <button className="show-more-button" onClick={showMoreItems}>
              Show More
            </button>
          </div>
        )}
      </div>
    </section>
  );
}

export default Filter;
