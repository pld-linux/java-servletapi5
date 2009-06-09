# TODO:
# - shouldn't it be java-servletapi-2.4 ?
#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc
%if "%{pld_release}" == "ti"
%bcond_without	java_sun	# build with gcj
%else
%bcond_with	java_sun	# use java-sun
%endif

%include	/usr/lib/rpm/macros.java

%define		srcname		servletapi5
Summary:	Java servlet and JSP implementation classes
Summary(pl.UTF-8):	Klasy z implementacją Java Servlet i JSP
Name:		java-servletapi5
Version:	5.5.27
Release:	6
License:	Apache v2
Group:		Libraries/Java
Source0:	http://www.apache.org/dist/tomcat/tomcat-5/v%{version}/src/apache-tomcat-%{version}-src.tar.gz
# Source0-md5:	eb3f196013550b9b1684e4ff18593a8e
Patch0:		jakarta-servletapi5-target.patch
# This patch is applied in tomcat svn. Remove it while upgrading to 5.5.28.
Patch1:		%{name}-CVE-2009-0781.patch
URL:		http://tomcat.apache.org/
BuildRequires:	ant
%{!?with_java_sun:BuildRequires:	java-gcj-compat-devel}
%{?with_java_sun:BuildRequires:	java-sun}
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	jpackage-utils
Provides:	jakarta-servletapi5
Provides:	jsp = 2.0
Provides:	servlet = 2.4
# for compatibility with some packages. But it is not true:
Provides:	servlet = %{version}
Provides:	servlet24
Provides:	servlet5
Provides:	servletapi = 2.4
Provides:	servletapi5
Obsoletes:	classpathx_servlet
Obsoletes:	jakarta-servletapi
Obsoletes:	jakarta-servletapi5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This subproject contains the compiled code for the implementation
classes of the Java Servlet and JSP APIs (packages javax.servlet,
javax.servlet.http, javax.servlet.jsp, and javax.servlet.jsp.tagext).

%description -l pl.UTF-8
Ten podprojekt zawiera skompilowany kod implementacji klas API Java
Servlet i JSP (pakiety javax.servlet, javax.servlet.http,
javax.servlet.jsp i java.servlet.jsp.tagext).

%package javadoc
Summary:	servletapi documentation
Summary(pl.UTF-8):	Dokumentacja do servletapi
Group:		Documentation
Requires:	jpackage-utils
Obsoletes:	jakarta-servletapi5-javadoc

%description javadoc
servletapi documentation.

%description javadoc -l pl.UTF-8
Dokumentacja do servletapi.

%prep
%setup -qc
mv apache-tomcat-%{version}-src/servletapi/* .
%patch0 -p2
%patch1 -p1

%build

%ant -f jsr154/build.xml dist \
	-Dbuild.compiler=extJavac \
	-Dservletapi.build=build \
	-Dservletapi.dist=dist

%ant -f jsr152/build.xml dist \
	-Dbuild.compiler=extJavac \
	-Dservletapi.build=build \
	-Dservletapi.dist=dist

%install
rm -rf $RPM_BUILD_ROOT

# JSP 2.0 and Servlet 2.4 classes
install -d $RPM_BUILD_ROOT%{_javadir}
cp -a jsr152/dist/lib/jsp-api.jar $RPM_BUILD_ROOT%{_javadir}/jsp-api-%{version}.jar
cp -a jsr154/dist/lib/servlet-api.jar $RPM_BUILD_ROOT%{_javadir}/servlet-api-%{version}.jar
ln -s servlet-api-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/servlet-api.jar
ln -s servlet-api-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/servlet.jar
ln -s jsp-api-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/jsp-api.jar

# not sure who expects what from which class
# servletapi4 contained both servlet-api and jsp-api classes in it's jar, so we link to api jar (or drop?)
ln -s servlet-api-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/servletapi5.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a jsr152/dist/docs/api $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}/jsp-api
cp -a jsr154/dist/docs/api $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}/servlet-api
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%{_javadir}/*.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
