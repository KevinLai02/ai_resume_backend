from ctransformers import AutoModelForCausalLM

alpaca = AutoModelForCausalLM.from_pretrained(
    "TheBloke/Chinese-Alpaca-2-13B-GGUF",
      model_file="chinese-alpaca-2-13b.q5_K_M.gguf", 
      model_type="alpaca"
    )