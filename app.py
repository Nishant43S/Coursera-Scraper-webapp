import streamlit as st      ## importing libraries
from streamlit_extras.colored_header import colored_header
from streamlit_option_menu import option_menu
from pyautoscraper.scraper import Scraper 
import requests



st.set_page_config(
    page_title="Courseera Scraper",
    page_icon="📑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

app_sidebar = st.sidebar   ### creating sidebar

with app_sidebar:
    
    st.text("")
    st.text("")
    st.text("")


    Main_menu = option_menu(  ### nav menu
        menu_title="",
        options=["Scraper","App Info"],
        icons=["file-code","person-circle"]
    )


if Main_menu == "Scraper":

    blank1 , app_column , blank2 = st.columns([2,8,2])

    with blank1:
        pass
    with blank2:
        pass


    with app_column:
        App_heading = colored_header(  ### app heading
            label="Coursera Scraper",
            color_name="violet-70",
            description="Find popular courses"   
        )
        st.text("")
        Search_item = st.text_input(  ### taking user input
            label="Enter Course name"
        )

        course_level_col , Duration_col , Sort_course_col = st.columns(3)
        with course_level_col:
            course_level = st.selectbox(
                label="Difficulty Level",
                options=["All Levels","Beginner","Advanced","Intermediate"],
                key="Difficulty level"
            )

            def Difficulty_level(text)->str:

                if text == "All Levels":
                    return ""
                
                elif text == "Beginner":
                    return "Beginner"
                
                elif text == "Advanced":
                    return "Advanced"
                
                elif text == "Intermediate":
                    return "Intermediate"

        with Duration_col:
            course_duration = st.selectbox(
                label="Duration",
                options=["All Durations","Less Than 2 Hours","1-4 Weeks","1-3 Months","3-6 Months","6-12 Months","1-4 Years"],
                key="duration"
            )


            def Course_duration(text):
                if text == "All Durations":
                    return text.replace("All Durations","")

                elif text == "Less Than 2 Hours":
                    return text.replace(" ","%20")
                
                elif text == "1-4 Weeks":
                    return text.replace(" ","%20")
                
                elif text == "1-3 Months":
                    return text.replace(" ","%20")
                
                elif text == "3-6 Months":
                    return text.replace(" ","%20")
                
                elif text == "6-12 Months":
                    return text.replace(" ","%20")
                
                elif text == "1-4 Years":
                    return text.replace(" ","%20")
                

        with Sort_course_col:
            Course_Sort_by = st.selectbox(
                label="Sort By",
                options=["Newest","Best Match"],
                index=1,
                key="Sort by"
            )
            def sort_item(Sort_text)->str:
                """
                this function make suitable
                string which is used in coursera website
                """
                if Sort_text == "Best Match":
                    return Sort_text.upper().replace(" ","_")
                elif Sort_text == "Newest":
                    return Sort_text[:3].upper()


        if st.button(label="Search Courses"):
        #### checking input is not empty
            if Search_item.strip() == "":
                st.success("Enter course Name",icon="✏️")

            else:
                st.subheader(f"Showing Results of {Search_item}")
                st.text("")
                Search_url = Search_item.replace(" ","%20")

                try:
                    url = requests.get(f"https://www.coursera.org/search?query={Search_url}") ### url of search
                    if url.status_code == 200:
                        print("Able to Scrape website")
                    else:
                        print("unable to Scrape website")
                except Exception as e:
                    st.warning("Sonething went wrong...\n\n",e)

                print(url.status_code)


                ###### main app
                try:
                    ### creating object
                    webscraper = Scraper(f'https://www.coursera.org/search?query={Search_url}&productDifficultyLevel={Difficulty_level(course_level)}&productDuration={Course_duration(course_duration)}&sortBy={sort_item(Course_Sort_by)}')  

                except Exception as err:
                    st.warning("Something went wrong...\n\n",err,icon="⚠️")

                ### app function
                def Course_Detail():
                    """
                    this function contains all data
                    releted to the course which are scraped from
                    coursera website
                    """
                    try:
                       
                        
                        course_heading = webscraper.findAll("h3",class_="cds-CommonCard-title css-6ecy9b")

                        company_name = webscraper.findAll("p",class_="cds-ProductCard-partnerNames css-vac8rf")

                        ratings =  webscraper.findAll("div",class_="cds-CommonCard-ratings")

                        skills_gain = webscraper.findAll("div",class_="cds-CommonCard-bodyContent")

                        course_dura = webscraper.findAll("div",class_="cds-CommonCard-metadata")

                        links = webscraper.findAll("a",class_="cds-119 cds-113 cds-115 cds-CommonCard-titleLink css-si869u cds-142")



                        ### itrating on list

                        for Heading, Company, rating, Skill, C_duration, Course_link in zip(
                            course_heading, company_name, 
                            ratings,skills_gain,
                            course_dura,links
                        ):

                            
                            st.markdown( ### displaying heading
                                f"""
                                <h5 class="h5-heading">{Heading.text}</h5>
                                """,
                                unsafe_allow_html=True
                            )

                            st.markdown( ### company names
                                f"""
                                <p style="font-weight: 500; font-size:16px;"><b>provided by - {Company.text}</b></p>
                                """,unsafe_allow_html=True
                            )

                            st.markdown( #### ratings
                                f"<p style='margin-top: 0px;'><b>{rating.text.replace("stars","⭐ ")[3:]}</b></p>",
                                unsafe_allow_html=True
                            )

                            st.text("")
                            st.text("Skills gained")
                            st.markdown(#### skills
                                Skill.text.replace("Skills you'll gain: ","")
                            )
                            st.text("")
                            st.markdown(C_duration.text)

                            Href_link = "https://www.coursera.org"+Course_link.get("href")
                            st.link_button(label="Visit Course",url=Href_link)

                            st.write("---")
                            st.text("")
                            st.text("")

                        
                    except Exception as err:
                        st.warning("wrong input")

                with st.spinner("Generating results..."):

                    if __name__=="__main__":
                        Course_Detail()  


def insert_html(file): ####m inserting external html
    with open(file) as f:
        st.markdown(f.read(),unsafe_allow_html=True)
    


if Main_menu == "App Info":
    b1 , about_column , b2 = st.columns([2,7,2])
    with b1:
        pass
    with b2:
        pass

    with about_column:
        if __name__=="__main__":
            insert_html("about_app.html")                   

def insert_css(file): ###### insert external css
    with open(file) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )
                
                

if __name__=="__main__":
    insert_css("style.css")