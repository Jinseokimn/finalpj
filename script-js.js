document.addEventListener('DOMContentLoaded', () => {
    const travelForm = document.getElementById('travel-form');
    const recommendationResult = document.getElementById('recommendation-result');

    travelForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        // 폼 데이터 수집
        const formData = {
            travel_style: document.getElementById('travel-style').value,
            destination: document.getElementById('destination').value,
            duration: parseInt(document.getElementById('duration').value),
            min_budget: parseInt(document.getElementById('min-budget').value),
            max_budget: parseInt(document.getElementById('max-budget').value)
        };

        recommendationResult.innerHTML = '<p>여행 추천을 생성 중입니다... 🌴</p>';

        try {
            // AI 추천 요청
            const response = await fetch('/recommend-travel-ai', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (data.ai_recommendation) {
                recommendationResult.innerHTML = `
                    <h3>🌍 여행 추천 결과</h3>
                    <p>${data.ai_recommendation.replace(/\n/g, '<br>')}</p>
                `;
            } else {
                recommendationResult.innerHTML = '<p>추천을 생성하는 데 실패했습니다. 다시 시도해주세요.</p>';
            }

        } catch (error) {
            console.error('Error:', error);
            recommendationResult.innerHTML = '<p>서버와 통신 중 오류가 발생했습니다.</p>';
        }
    });
});
