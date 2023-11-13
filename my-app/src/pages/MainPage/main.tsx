import React, { useEffect, useState } from 'react';
import { ChangeEvent } from 'react';
import { Link } from 'react-router-dom';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Dropdown from 'react-bootstrap/Dropdown';
import Header from '../../components/header';
import OneCard from '../../components/card';
import styles from './main.module.scss';

export type Vacancies = {
    id: number,
    title: string,
    adress?: string |null,
    time: string,
    salary: number,
    company: string,
    city?: string | null,
    exp: string,
    image?: string | null,
    info?: string,
    status: string
}

export type ReceivedVacancyData = {
    id: number,
    title: string,
    salary: number,
    city: string,
    company: string,
    exp: string | undefined | null,
    image: string | undefined | null;
}

const mockVacancies = [
    {'title': 'Копирайтер', 'adress': 'Алексеевская', 'time':'Полный день', 'salary': 50000, 'company': 'Копи-копи', 'city': 'Москва', 'exp': 'Без опыта', 'image': "https://w7.pngwing.com/pngs/299/589/png-transparent-social-media-computer-icons-technical-computer-network-text-computer.png", 'id': 1, 'status': 'enabled', 'info': 'Компания "Копи-копи" стремится к совершенству и инновациям. Ее команда талантливых копирайтеров постоянно ищет новые способы выразить идеи и повысить эффективность коммуникации. С каждым текстом, созданным "Копи-копи", они продолжают укреплять свою репутацию как надежного партнера, который доставляет не только качественные тексты, но и вдохновение, которое воплощается в каждом слове.','requirements' :['Отличное владение русским языком', 'Умение писать грамотные тексты', 'Креативность и внимательность к деталям'], 'conditions': ['Гибкий график работы', 'Возможность удаленной работы', 'Оплачиваемый отпуск', 'Профессиональное развитие и обучение', 'Дружеская и поддерживающая рабочая атмосфера']},
    {
    'title': 'Менеджер блогера',
    'adress': 'Алтуфьевское шоссе, 12',
    'time': 'Сменный график',
    'salary': 10000,
    'company': 'Co_blog',
    'city': 'Москва',
    'exp': 'От года',
    'image': null,
    'id': 2,
    'status': 'enabled',
    'info': 'Компания Co_blog - это легендарный блогинговый ресурс, который начал свою деятельность двадцать лет назад в гараже основателя. С течением времени они стали одной из самых влиятельных и популярных платформ для блогеров. Co_blog известен своим инновационным подходом к созданию контента и использованию социальных сетей для его продвижения. Сотрудники компании являются настоящими экспертами в области блогинга и имеют огромную базу фанатов и подписчиков, которые следят за их публикациями. Co_blog стал не только платформой для создания и обмена контентом, но и местом, где талантливые блогеры могут раскрыть свой потенциал и достичь большого успеха.',
    },
    {
    'title': 'Куратор',
    'salary': 7000,
    'time': 'Удаленная работа',
    'company': 'Вебскул',
    'image': 'https://cdn1.dizkon.ru/images/contests/2017/08/15/5992c98e5cd2e.700x534.80.jpg',
    'exp': 'Без опыта',
    'id': 3,
    'status': 'enabled',
    'info': 'Вебскул - компания, которая изменила пейзаж онлайн-образования. Они были основаны группой страстных преподавателей и разработчиков, которые верили в доступность и качество образования для всех. Вебскул разработал инновационную веб-платформу, которая объединяет учителей и учеников со всего мира. С помощью передовых технологий и интерактивных методик обучения, Вебскул предлагает образовательные курсы в различных областях знаний. Компания стремится изменить способ, которым люди учатся и развиваются, и дает возможность каждому раскрыть свой потенциал независимо от места проживания или времени.',
    },
    {
    'title': 'Редактор',
    'salary': 20000,
    'time': 'Удаленная работа',
    'company': 'Новая газета',
    'city': 'Москва',
    'exp': 'Без опыта',
    'id': 4,
    'status': 'enabled',
    'info': 'Новая газета - это историческое издание, которое существует уже более ста лет. Они являются одним из самых авторитетных и влиятельных печатных изданий в стране. Новая газета всегда была символом независимой журналистики и свободы слова. Их журналисты и редакторы известны своей профессиональностью, точностью и честностью в отношении информации, которую они предоставляют своим читателям. Новая газета активно освещает важные события и проблемы общества, их репортажи и статьи часто становятся объектом обсуждения и влияют на общественное мнение.',
    }
]



const MainPage: React.FC = () => {
    const [vacancies, setVacancies] = useState<Vacancies[]>([]);
    const [titleValue, setTitleValue] = useState<string>('')

    const fetchVacancies = async () => {
        let response = null;
        let url = 'http://localhost:8000/vacancies'

        if (titleValue) {
            url += `?keyword=${titleValue}`
        }
        console.log(url)
        try {
            response = await fetch(url);

            const jsonData = await response.json();
            const newVacanciesArr = jsonData.map((raw: ReceivedVacancyData) => ({
                id: raw.id,
                title: raw.title,
                salary: raw.salary,
                city: raw.city,
                company: raw.company,
                image: raw.image,
                exp: raw.exp
            }))
            setVacancies(newVacanciesArr);
        }
        catch {
            if (titleValue) {
                const filteredArray = mockVacancies.filter(mockVacancies => mockVacancies.title.includes(titleValue));
                setVacancies(filteredArray);
            } else {
                setVacancies(mockVacancies);
            }

        }
        
    };

    useEffect(() => {
        fetchVacancies();
    }, []);

    const handleSearchButtonClick = () => {
        fetchVacancies();
    }

    const handleTitleValueChange = (event: ChangeEvent<HTMLInputElement>) => {
        setTitleValue(event.target.value);
    };

    
    // const handleFormSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    //     event.preventDefault();
    // };

    return (
        <div className={styles.main_page}>
            <Header/>
            <nav aria-label="breadcrumb">
            <ol className="breadcrumb" style={{ marginTop: '80px' , width: '95.53vw', maxHeight: '100vw'}}>
            <li className="breadcrumb-item">
                <Link style={{ color: 'rgb(0, 102, 255)' }} to="/vacancies">
                Список вакансий
                </Link>
            </li>
            <div style={{ display: 'flex', justifyContent: 'center' }}>
            <Form.Group controlId="name">
                <Form.Control
                type="text"
                placeholder="Введите название вакансии"
                style={{
                    backgroundColor: 'rgb(231, 230, 230)',
                    height: '30px',
                    width: '60vw',
                    fontSize: '18px',
                    border: 'none',
                    outline: 'none',
                    marginRight: '5px',
                    textAlign: 'center',
                }}
                onChange={handleTitleValueChange}
                />
            </Form.Group>
            <Button
                variant="primary"
                type="submit"
                style={{
                color: 'white',
                backgroundColor: 'rgb(0, 102, 255)',
                border: 'none',
                height: '30px',
                fontSize: '15px',
                borderRadius: '10px',
                width: '200px',
                marginLeft: '20px',
                fontFamily: 'sans-serif',
                justifyContent: 'center', // Center the text horizontally
                alignItems: 'center', // Center the text vertically
                }}
                onClick={() => handleSearchButtonClick()}
            >
                Поиск
            </Button>
            </div>
            </ol>
            </nav>
            <div className={styles["hat"]}>

                    <div className={styles["cards"]}>
                        {
                        vacancies.map((vacancy: Vacancies) => (
                            <div className='card'>
                            <OneCard id={vacancy.id} image={vacancy.image} salary={Number(vacancy.salary)} title={vacancy.title} city={vacancy.city} company={vacancy.company} exp={vacancy.exp} onButtonClick={() => console.log('add to application')}></OneCard>
                            </div>
                        ))}
                    </div>
                {vacancies.length === 0 && <p className="dish-text"> <big>Такой вакансии не существует</big></p>}
            </div>
        </div>
     )
};
  
export default MainPage;