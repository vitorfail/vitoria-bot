const express = require('express');
const axios = require('axios');
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware para permitir o processamento de JSON
app.use(express.json());

app.post('/login', async (req, res) => {
    const username = "GilmaraCimas405"
    const password = "42cVYRToTuG"

    try {
        const loginPageResponse = await axios.get("https://www.instagram.com/accounts/login/", {
            headers: {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept": "application/json, text/javascript, */*; q=0.01"
            },
            maxRedirects: 0, // Para não seguir redirecionamentos
            validateStatus: false // Para capturar todos os status de resposta
        });

        // Obtendo o CSRF token dos cookies
        const cookies = loginPageResponse.headers['set-cookie'];
        const csrfToken = cookies.find(cookie => cookie.startsWith('csrftoken=')).split('=')[1];

        // Configurando os headers para a solicitação de login
        const headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": cookies.join('; ') // Inclui os cookies na requisição
        };

        // Dados para o login
        const data = new URLSearchParams({
            username: username,
            password: password
        });

        // Realizando a solicitação de login
        const loginResponse = await axios.post("https://www.instagram.com/accounts/login/ajax/", data.toString(), {
            headers: headers,
            maxRedirects: 0,
            validateStatus: false
        });

        const result = loginResponse.data;

        if (result.authenticated) {
            res.json({ message: "Login bem-sucedido!", result });
        } else {
            res.status(401).json({ message: "Falha no login", error: result.message });
        }
    } catch (error) {
        console.error("Erro ao fazer login:", error);
        res.status(500).json({ message: "Erro ao realizar a requisição", error: error.message });
    }
});

app.listen(PORT, () => {
    console.log(`Servidor rodando em http://localhost:${PORT}`);
});
