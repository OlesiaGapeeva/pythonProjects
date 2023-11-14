import {Routes, Route } from 'react-router-dom'
import MainPage from './pages/MainPage/main';
import DetaliedPage from './pages/DetailedPage/detailed';

function App() {
  return (
    <div className='app'>
        <Routes>
          <Route path="/" element={<h1>Это наша стартовая страница</h1>} />
          <Route path="/vacancies" element={<MainPage />} />

          <Route path="/vacancies/:id" element={<DetaliedPage />} />
        </Routes>
    </div>
  );
}
  
export default App;