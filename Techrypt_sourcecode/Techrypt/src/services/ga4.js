import GA4React from "ga-4-react";

// Handle environment variables for both Vite and Create React App
const MEASUREMENT_ID = (() => {
  try {
    return import.meta.env?.VITE_GA4_MEASUREMENT_ID || 
           (typeof process !== 'undefined' ? process.env?.REACT_APP_GA4_MEASUREMENT_ID : null);
  } catch (error) {
    return import.meta.env?.VITE_GA4_MEASUREMENT_ID || null;
  }
})();

class GA4Service {
  constructor() {
    this.ga4react = null;
    this.isInitialized = false;
  }

  async initialize() {
    if (!MEASUREMENT_ID) {
      console.warn('GA4 Measurement ID not found');
      return;
    }

    try {
      this.ga4react = new GA4React(MEASUREMENT_ID);
      await this.ga4react.initialize();
      this.isInitialized = true;
      console.log('GA4 initialized successfully');
    } catch (error) {
      console.error('GA4 initialization failed:', error);
    }
  }

  pageview(path) {
    if (this.isInitialized && this.ga4react) {
      this.ga4react.pageview(path);
    }
  }

  event(action, parameters = {}) {
    if (this.isInitialized && this.ga4react) {
      this.ga4react.event(action, parameters);
    }
  }
}

export default new GA4Service();