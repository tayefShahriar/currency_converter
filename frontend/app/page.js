"use client"
import axios from "axios";
import Image from 'next/image'
import styles from './page.module.css'
import { useEffect, useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";


export default function Home() {
  const [currencies, setCurrencies] = useState([])
  const [fromCurrency, setFromCurrency] = useState('USD');
  const [toCurrency, setToCurrency] = useState('USD');
  const [amount, setAmount] = useState('');
  const [convertedResult, setConvertedResult] = useState(null);

  useEffect(() => {
    axios.get('http://localhost:8000/api/currencies')
    .then(response => setCurrencies(response.data))
    .catch(error => console.error('Error fetching currencies: ', error))
  }, []);

  const convertCurrency = () => {
    axios.get(`http://localhost:8000/api/convert/${fromCurrency}/${toCurrency}/${amount}`)
    .then(response => setConvertedResult(response.data.converted_amount))
    .catch(error => console.log('error converting currency:', error))
  }

  return (
    <div className="container d-flex justify-content-center align-items-center vh-100">
      <div className="bg-light py-5 border border-3 rounded-5 shadow-lg px-5 col-9">
        <h1 className="text-center mb-5">FX Currency Convertor</h1>

        <div className="d-flex">
          <div className="col-6 px-3">
            <h3>From</h3>
            <select className="form-select form-select-lg mb-3" onChange={e => setFromCurrency(e.target.value)}>
              {currencies.map(currency => <option key={currency.code} value={currency.code}>{currency.code}</option>)}
            </select>
          </div>
          <div className="col-6 px-3">
            <h3>To</h3>
            <select className="form-select form-select-lg mb-3" onChange={e => setToCurrency(e.target.value)}>
              {currencies.map(currency => <option key={currency.code} value={currency.code}>{currency.code}</option>)}
            </select>
          </div>
        </div>
        <div className="px-3 mt-3 mb-5">
          <h3>Amount</h3>
          <input type="number" className="form-control form-control-lg mb-3" onChange={e => setAmount(e.target.value)} />
          <button className="btn btn-success" onClick={convertCurrency}>Convert</button>
        </div>
        {convertedResult && <p className="fs-3">{amount} {fromCurrency} = {convertedResult} {toCurrency}</p>}
      </div>
    </div>
  )
}

