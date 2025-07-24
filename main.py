from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.chat import ChatRequest, ChatResponse
from app.services.market_data import get_stock_price

app = FastAPI()

# CORS middleware to allow frontend to communicate with backend
app.add_middleware(
	CORSMiddleware,
	allow_origins=["http://localhost:3000"],  # Allow your frontend origin
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)

@app.get("/")
async def read_root():
	return {"message": "Welcome to Dalaal Street Bot API"}

@app.post("/chat", response_model=ChatResponse)
async def chat_with_bot(request: ChatRequest):
	user_message = request.message.lower()
	response_text = "I'm sorry, I don't understand that. Please ask about stock prices or general financial terms."

	if "price of" in user_message:
		parts = user_message.split("price of ")
		if len(parts) > 1:
			symbol = parts[1].strip().upper()
			stock_info = get_stock_price(symbol)
			if "price" in stock_info:
				response_text = f"The current price of {stock_info['symbol']} is {stock_info['price']:.2f} INR."
			else:
				response_text = stock_info['error']
	elif "hello" in user_message or "hi" in user_message:
		response_text = "Hello! How can I help you with Indian financial markets today?"
	elif "what is" in user_message:
		response_text = "That's a good question! I'm still learning about financial terminology. Can you be more specific?"

	return ChatResponse(response=response_text)