import React from 'react';
import Button from 'react-bootstrap/Button';
import Image from 'react-bootstrap/Image'
import Card from 'react-bootstrap/Card';
import { Link } from 'react-router-dom';
import styles from './card.module.scss';

export type CardProps = {
  id: number,
  image?: string | null;
  title: string;
  salary: number;
  city: React.ReactNode;
  company: string;
  exp: string;
  onButtonClick?: React.MouseEventHandler;
  onImageClick?: React.MouseEventHandler;
};

const OneCard: React.FC<CardProps> = ({id, title, salary, city, company, image, exp, onButtonClick, onImageClick }) => {
  return (
    <Card className={styles.card}>
        <div>
        
        <Image className={styles.image}
          onClick={onImageClick}
          src={image ? image : "https://www.solaredge.com/us/sites/nam/files/Placeholders/Placeholder-4-3.jpg"}
        />

        </div>
      
      <Card.Body>
        <div>
        <Link to={`/vacancies/${id}`} style={{ textDecoration: 'none', color: '#0066ff' }}>
        
        <h2 style={{ paddingLeft: '20px' }}>{title}</h2>
            </Link>  
            <h3 style={{ paddingLeft: '20px' }}>{salary}</h3>         
        </div>
        <p> <div style={{ paddingLeft: '20px' }}>{company}</div>
      <div style={{ paddingLeft: '20px' }}>{city}</div> </p>
      <p style={{ paddingLeft: '20px'}}>
      <span style={{ display: 'inline-flex', alignItems: 'center', gap: '7 px'}}>
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16" style={{ marginRight: '7px' }}>
          <path d="M6.5 1A1.5 1.5 0 0 0 5 2.5V3H1.5A1.5 1.5 0 0 0 0 4.5v1.384l7.614 2.03a1.5 1.5 0 0 0 .772 0L16 5.884V4.5A1.5 1.5 0 0 0 14.5 3H11v-.5A1.5 1.5 0 0 0 9.5 1h-3zm0 1h3a.5.5 0 0 1 .5.5V3H6v-.5a.5.5 0 0 1 .5-.5z"/>
          <path d="M0 12.5A1.5 1.5 0 0 0 1.5 14h13a1.5 1.5 0 0 0 1.5-1.5V6.85L8.129 8.947a.5.5 0 0 1-.258 0L0 6.85v5.65z"/>
        </svg>
        {exp}
      </span>
    </p>
      <div style={{ paddingLeft: '20px' }}>
      <button type="button" className={styles.btn_apply} onClick={onButtonClick}>Откликнуться</button>
      </div>
        <div className='mt-auto'>
        </div>
      </Card.Body>
    </Card>
  );
};

export default OneCard;