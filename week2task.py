{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "50a31ad6-4945-407f-828f-0fccefda2789",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0    1\n",
       "1    2\n",
       "2    3\n",
       "3    4\n",
       "4    5\n",
       "dtype: int64"
      ]
     },
     "execution_count": 1,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "import pandas as pd\n",
    "lst=[1,2,3,4,5]\n",
    "df=pd.Series(lst)\n",
    "df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "id": "57361d95-7f67-478d-b115-9bac4468ad36",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'pandas.core.frame.DataFrame'>\n",
      "RangeIndex: 5 entries, 0 to 4\n",
      "Data columns (total 4 columns):\n",
      " #   Column   Non-Null Count  Dtype \n",
      "---  ------   --------------  ----- \n",
      " 0   Name     5 non-null      object\n",
      " 1   class    5 non-null      object\n",
      " 2   Subject  5 non-null      object\n",
      " 3   Rollno   5 non-null      int64 \n",
      "dtypes: int64(1), object(3)\n",
      "memory usage: 292.0+ bytes\n"
     ]
    }
   ],
   "source": [
    "md=pd.read_csv(r\"C:\\Users\\vinne\\OneDrive\\Desktop\\groudetail.csv\")\n",
    "md.info()\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "63b6e3b9-db14-4b0f-ab96-bb33d64bf698",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Name</th>\n",
       "      <th>class</th>\n",
       "      <th>Subject</th>\n",
       "      <th>Rollno</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>vinay</td>\n",
       "      <td>Btech</td>\n",
       "      <td>ML</td>\n",
       "      <td>31</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>vikas</td>\n",
       "      <td>Btech</td>\n",
       "      <td>ML</td>\n",
       "      <td>32</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>vishnavi</td>\n",
       "      <td>Btech</td>\n",
       "      <td>ML</td>\n",
       "      <td>33</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>vivek</td>\n",
       "      <td>Btech</td>\n",
       "      <td>ML</td>\n",
       "      <td>34</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>vijay</td>\n",
       "      <td>Btech</td>\n",
       "      <td>ML</td>\n",
       "      <td>35</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "       Name  class Subject  Rollno\n",
       "0     vinay  Btech      ML      31\n",
       "1     vikas  Btech      ML      32\n",
       "2  vishnavi  Btech      ML      33\n",
       "3     vivek  Btech      ML      34\n",
       "4     vijay  Btech      ML      35"
      ]
     },
     "execution_count": 4,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "md.shape\n",
    "md"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "7a2b08bc-e696-4aaa-ae2a-66f75ba26df2",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.2"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
