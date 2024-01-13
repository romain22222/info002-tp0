# TP0 - The forgotten : Playfair

## Utilisation

`python3 main.py <CMD> [ARGS]`

Pour plus d'informations, voir `python3 main.py help`

Exemples :
- `python3 main.py key microphone`
- `python3 main.py fitness test.txt`
- `python3 main.py encipher test.txt test_encrypted.txt microphone`
- `python3 main.py decipher test_encrypted.txt test_decrypted.txt microphone`
- `python3 main.py crack hill test_encrypted.txt test_decrypted.txt LIDROPHNEABCFGKMQSTUVWYXZ 50000`
- `python3 main.py crack hill test_encrypted.txt test_decrypted.txt`
- `python3 main.py crack recuit test_encrypted.txt test_decrypted.txt LIDROPHNEABCFGKMQSTUVWYXZ 50000 60 0.2 0.01`
- `python3 main.py crack recuit test_encrypted.txt test_decrypted.txt`

Attention les versions par défaut de la commande crack va (très souvent) donner des résultats faux.