import streamlit as st

from ml_app import run_ml_app

def main():
    menu = ['Home', 'Predict Churn Customer']
    choice = st.sidebar.radio("Menu", menu)

    if choice == 'Home':
            st.markdown(
            '''
            <h1 style='text-align: center;'> Predicting Churn Can Improve Customer Retention </h1>
            <br>
            <p style='text-align: justify;'> Preventing customers from leaving your service is key to maintaining sustainable growth. With our churn prediction tool, you can better understand customer behavior and take more targeted actions to improve retention. By predicting customer churn, you can:</p>
                <ul style='text-align: justify;'>
                    <li><strong>Increase Customer Retention:</strong> Reduce customer churn rates and ensure stronger long-term relationships. </li>
                    <li><strong>Maximize Customer Lifetime Value (CLV):</strong> Focus on customers with higher value potential, increasing long-term revenue. </li>
                    <li><strong>Improved Customer Satisfaction:</strong> By understanding customer needs and preferences, you can offer a more satisfying and relevant experience. </li>
                </ul>
            </p>
            <br>
            <p style='text-align: justify;'><strong>Disclaimer:</strong> This tool is only to help you in analyzing customer data and may make analysis errors. Do further analysis to minimize errors. </p>
            <br>
            <p style='text-align: center;'><strong>Since the customer is king, retain them better.</strong></p>
            ''',
            unsafe_allow_html=True
        )
    elif choice == 'Predict Churn Customer':
        run_ml_app()


if __name__ == '__main__':
    main()
